import threading
import logging
import time


def thread_func(name):
    logging.info("thread %s: staring", name)
    time.sleep(2)
    logging.info("thread %s: finishing", name)


if __name__ == "__main__":
    format = "%(asctime)s : %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    logging.info("main: before creating thread")
    x = threading.Thread(target=thread_func, args=(1, ))
    logging.info("main: before running thread")
    x.start()
    logging.info("main: waiting for thread to finish")
    logging.info("main: all done")
