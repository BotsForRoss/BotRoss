import patcher
patcher.patch()

import cnc.main  # noqa: E402

if __name__ == '__main__':
    cnc.main.main()
