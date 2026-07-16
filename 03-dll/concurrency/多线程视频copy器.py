import threading
import os
import time


def copy_file(file_name, source_dir, dest_dir):
    
    source_path = os.path.join(source_dir, file_name)
    dest_path = os.path.join(dest_dir, file_name)

    with open(source_path, "rb") as source_file:
        with open(dest_path, "wb") as dest_file:

            while True:

                data = source_file.read(1024)

                if data:
                    dest_file.write(data)

                else:
                    break



if __name__ == "__main__":

    source_dir = r"c:\Users\zigyr\desktop\1"
    dest_dir = r"c:\Users\zigyr\desktop\2"

    file_list = os.listdir(source_dir)

    start = time.time()

    # 并发copy
    for file_name in file_list:  # 0.00293

        sub_thread = threading.Thread(target=copy_file, args=(file_name, source_dir, dest_dir))

        sub_thread.start()
    
    end = time.time()
    print(f"{end - start : .5f}")