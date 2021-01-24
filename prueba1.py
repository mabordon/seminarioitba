from itbatools import get_itba_logger


l1=get_itba_logger("prueba",True)
l2=get_itba_logger("Tarola",True)
l3=get_itba_logger("Tarola",True)
print(l1==l2)
print(l1.__dict__)
print(l2.__dict__)
print("Comparando l2 con l3")
#print(l2==l3)

l1.info("Soy log1")
l2.info("Soy log2")
l2.warning("Soy un warning")
l1.error("Soy un error")
l1.error("Error")

