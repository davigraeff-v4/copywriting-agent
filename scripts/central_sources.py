#!/usr/bin/env python3
"""Read only this Central task's snapshots. No network, gws or Google token."""
import argparse
import json
import os
from pathlib import Path
import sys
import time
import uuid


def regular(path, limit):
    if path.is_symlink() or not path.is_file() or path.stat().st_size>limit:
        raise ValueError('source_reader_file_unavailable')
    return path.read_bytes()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation',choices=['inspect','list','find','read','manifest'])
    parser.add_argument('value',nargs='?')
    parser.add_argument('--cursor',type=int,default=0)
    parser.add_argument('--failure-cursor',type=int,default=0)
    args=parser.parse_args()
    output_emitted=False
    try:
        path=Path(os.environ.get('CENTRAL_SOURCE_READER_CONTEXT',''))
        if not path.is_absolute() or path.resolve()!=path or path.stat().st_mode&0o077:
            raise ValueError('source_reader_context_unavailable')
        context=json.loads(regular(path,4096));folder=path.parent
        if context['queue']!=str(folder) or len(context['token'])!=64:
            raise ValueError('source_reader_context_unavailable')
        def request(payload):
            nonce=uuid.uuid4().hex;pending=folder/('pending-'+nonce+'.json');target=folder/('request-'+nonce+'.json')
            raw=json.dumps({'token':context['token'],'request':payload}).encode()
            if len(raw)>4096: raise ValueError('source_reader_request_limit')
            descriptor=os.open(pending,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
            with os.fdopen(descriptor,'wb') as stream: stream.write(raw);stream.flush();os.fsync(stream.fileno())
            pending.rename(target)
            response=folder/('response-'+nonce+'.json');deadline=time.monotonic()+(25 if payload.get('operation')=='read' else 5)
            while not response.exists():
                if time.monotonic()>=deadline: raise ValueError('source_reader_timeout')
                time.sleep(.02)
            result=json.loads(regular(response,1048576))
            if not result['ok']: raise ValueError('source_reader_refused')
            return result['result']
        body={'operation':args.operation,'cursor':args.cursor,'failure_cursor':args.failure_cursor}
        if args.value is not None: body['query' if args.operation=='find' else 'id']=args.value
        result=request(body)
        if args.operation=='read':
            receipt=result.pop('receipt')
            print(json.dumps(result,ensure_ascii=False,indent=2),flush=True)
            output_emitted=True
            request({'operation':'ack','receipt':receipt})
        else:
            print(json.dumps(result,ensure_ascii=False,indent=2),flush=True)
        return 0
    except BrokenPipeError:
        return 2
    except (OSError,ValueError,KeyError):
        print(json.dumps({'status':'blocked','error':'source_reader_unavailable_or_outside_scope'}),
              file=sys.stderr if output_emitted else sys.stdout)
        return 2


if __name__=='__main__': sys.exit(main())
