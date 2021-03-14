from conf.test import workdir
import os
import src.banner.home as banner
from src.utils.utils import loads_env

def main():
	ctx = loads_env()
	banner.menu(ctx)


if __name__ == '__main__':
	os.chdir(workdir)
	main()

