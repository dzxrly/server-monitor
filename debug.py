import argparse

from app import app

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', '-d', type=bool, default=True, help='是否开启调试模式')

    args = parser.parse_args()
    app.run(debug=args.debug, host='0.0.0.0')
