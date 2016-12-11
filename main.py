import queue
import _thread
import urllib.request
import configparser
import xml.etree.ElementTree as et

q = queue.Queue()
config = configparser.ConfigParser()
cmd = ""

def worker(threadName, _api):
    api = _api.strip()
    global cmd
    
    while cmd.lower() != "quit":
        if not q.empty():
            code = q.get(True, 50).strip()
            output = urllib.request.urlopen("http://api.upcdatabase.org/xml/" + api + "/" + code).read()
            data = et.fromstring(output)
                        
            if str(data[0].text).lower() == "true":
                name = data[2].text
                desc = data[4].text
    
                if name is None or len(name) <= 0:
                    if desc is None or len(desc) <= 0:
                        name = "Unknown Product: " + code
                    else:
                        name = desc.strip()

                print(name)
            else:
                print("Unregistered Product: " + code)

def scanner():
    global cmd
    while cmd.lower() != "quit":
        cmd = input()
        q.put(cmd, True, 50)

def main():
    config.read("config.ini")
    api = str(config["upcdatabase"]["api"])
    
    print("Program started...")
    worker_thread = _thread.start_new_thread(worker, ("worker", api))
    scanner() # This contains loop for main thread

if __name__ == "__main__":
    main()
