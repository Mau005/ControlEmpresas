import threading


class Prueba(threading.Thread):
    
    def __init__(self):
        super(Prueba,self).__init__()
        
        
        

    def run(self):
        contador = 0
        while True:
            contador +=1
            if contador >= 1000:
                break
        
        self.join()
        
        
        
test =Prueba()
test.start()