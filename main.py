from WindowDark import WindowDark
import time
import UI


if __name__=='__main__':
    root=WindowDark(480,700,0,0)
    main_queue=UI.Queue(root.root)

    last_t=time.time()
    delta_t=0

    while True:
        main_queue.update(delta_t)
        root.root.update()

        t=time.time()
        delta_t=t-last_t
        last_t=t