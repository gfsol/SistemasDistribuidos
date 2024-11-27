import sys
import Ice
import RemoteTypes

class Client(Ice.Application):
    def run(self, args):
        proxy = self.communicator().stringToProxy("factory:tcp -h localhost -p 4062")
        factory = RemoteTypes.FactoryPrx.checkedCast(proxy)

        if not factory:
            raise RuntimeError("Proxie invalido")

        rlist = factory.get(RemoteTypes.TypeName.RList, "Ejemplo de lista")
        rlist = RemoteTypes.RListPrx.checkedCast(rlist)

        rset = factory.get(RemoteTypes.TypeName.RSet, "Ejemplo de set")
        rset = RemoteTypes.RSetPrx.checkedCast(rset)

        rdict = factory.get(RemoteTypes.TypeName.RDict, "Ejemplo de diccionario")
        rdict = RemoteTypes.RDictPrx.checkedCast(rdict)

        if not rlist or not rset or not rdict:
            raise RuntimeError("Proxie invalido")

        # Operaciones con RDict
        rdict.setItem("key1", "value1")
        rdict.setItem("key2", "value2")
        print("RDict getItem('key1'):", rdict.getItem("key1"))

        # Iterar sobre RDict
        print("Iterando sobre RDict:")
        iterable = rdict.iter()
        try:
            while True:
                print(iterable.next())
        except RemoteTypes.StopIteration:
            print("Fin de la iteración de RDict")
        except RemoteTypes.CancelIteration:
            print("Iteración cancelada debido a modificación")

        # Operaciones con RSet
        rset.add("item1")
        rset.add("item2")
        rset.add("item3")
        rset.add("item4")

        # Iterar sobre RSet
        print("Iterando sobre RSet:")
        iterable = rset.iter()
        try:
            while True:
                print(iterable.next())
        except RemoteTypes.StopIteration:
            print("Fin de la iteración de RSet")
        except RemoteTypes.CancelIteration:
            print("Iteración cancelada debido a modificación")

        # Operaciones con RList
        rlist.append("item1")
        rlist.append("item2")
        rlist.append("item3")
        rlist.append("item4")
        print("RList getItem(0):", rlist.getItem(0))
        print("RList pop(0):", rlist.pop(0))

        # Iterar sobre RList
        print("Iterando sobre RList:")
        iterable = rlist.iter()
        try:
            while True:
                print(iterable.next())
        except RemoteTypes.StopIteration:
            print("Fin de la iteración de RList")
        except RemoteTypes.CancelIteration:
            print("Iteración cancelada debido a modificación")

if __name__ == "__main__":
    for _ in range(2): # Se ejecuta dos veces para probar la cancelación de la iteración
        app = Client()
        sys.exit(app.main(sys.argv, "client.config"))
