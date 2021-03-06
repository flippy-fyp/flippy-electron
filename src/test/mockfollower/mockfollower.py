import sys
import argparse
import time
import socket

HOST = "127.0.0.1"
PORT = 60000

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def encode_str(x: str) -> bytes:
    return x.encode()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Mock follower for testing'
    )

    parser.add_argument(
        '--ready',
        type=float,
        help='The time (in seconds) before READY is output',
        default=1.0,
    )    
    parser.add_argument(
        '--interval',
        type=float,
        help='The interval (in seconds) between two prints',
        default=1.0,
    )
    parser.add_argument(
        '--diff',
        type=float,
        help='The number (in seconds) to increment each printed number',
        default=0.1,
    )
    parser.add_argument(
        '--limit',
        type=int,
        help='The number of number prints before exiting',
        default=50,
    )
    parser.add_argument(
        '--startnum',
        type=float,
        help='Start value',
        default=0.0,
    )

    args = parser.parse_args()

    ready = args.ready
    interval = args.interval
    diff = args.diff
    limit = args.limit
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        eprint('started')
        eprint(f"{HOST}:{PORT}")
        time.sleep(ready)
        s.sendto(encode_str('READY'), (HOST, PORT))

        acc = args.startnum
        for i in range(limit):
            s.sendto(encode_str(f'{acc}'), (HOST, PORT))
            eprint(acc)
            time.sleep(interval)
            acc += diff
        
        s.close()
