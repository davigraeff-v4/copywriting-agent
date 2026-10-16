import Foundation
import Vision
import ImageIO
struct Row: Codable { let text:String; let confidence:Float; let box:[Double] }
struct Result: Codable { let path:String; let width:Int; let height:Int; let rows:[Row]; let error:String? }
let paths=Array(CommandLine.arguments.dropFirst())
for path in paths {
    do {
        let url=URL(fileURLWithPath:path)
        guard let source=CGImageSourceCreateWithURL(url as CFURL,nil), let cg=CGImageSourceCreateImageAtIndex(source,0,nil) else {throw NSError(domain:"OCR",code:1)}
        var work=cg
        if cg.width<700 {
            let scale=3
            if let ctx=CGContext(data:nil,width:cg.width*scale,height:cg.height*scale,bitsPerComponent:8,bytesPerRow:0,space:CGColorSpaceCreateDeviceRGB(),bitmapInfo:CGImageAlphaInfo.premultipliedLast.rawValue) {
                ctx.interpolationQuality = .high
                ctx.draw(cg,in:CGRect(x:0,y:0,width:cg.width*scale,height:cg.height*scale))
                if let enlarged=ctx.makeImage(){work=enlarged}
            }
        }
        var rows:[Row]=[]
        let bands = work.height>2500 ? stride(from:0,to:work.height,by:1500).map { $0 } : [0]
        for top in bands {
            let height=min(work.height-top,work.height>2500 ? 1700 : work.height)
            guard let tile=work.cropping(to:CGRect(x:0,y:top,width:work.width,height:height)) else{continue}
            let request=VNRecognizeTextRequest()
            request.recognitionLevel = .accurate
            request.usesLanguageCorrection = true
            request.recognitionLanguages = ["en-US","pt-BR"]
            request.automaticallyDetectsLanguage = true
            request.minimumTextHeight = 0.003
            request.usesCPUOnly = true
            try VNImageRequestHandler(cgImage:tile,options:[:]).perform([request])
            for o in request.results ?? [] {
                guard let c=o.topCandidates(1).first else{continue}
                let b=o.boundingBox
                let box=[Double(b.minX),(Double(work.height-top-height)+Double(b.minY)*Double(height))/Double(work.height),Double(b.width),Double(b.height)*Double(height)/Double(work.height)]
                let row=Row(text:c.string,confidence:c.confidence,box:box)
                if let index=rows.firstIndex(where:{$0.text==row.text && abs($0.box[1]-row.box[1])<0.015 && abs($0.box[0]-row.box[0])<0.03}) {
                    if row.confidence>rows[index].confidence{rows[index]=row}
                } else {rows.append(row)}
            }
        }
        rows.sort { a,b in
            let ay=a.box[1]+a.box[3]/2;let by=b.box[1]+b.box[3]/2
            return abs(ay-by)>0.008 ? ay>by : a.box[0]<b.box[0]
        }
        let result=Result(path:path,width:cg.width,height:cg.height,rows:rows,error:nil)
        let data=try JSONEncoder().encode(result)
        print(String(data:data,encoding:.utf8)!)
    } catch {
        let data=try! JSONEncoder().encode(Result(path:path,width:0,height:0,rows:[],error:String(describing:error)))
        print(String(data:data,encoding:.utf8)!)
    }
}
