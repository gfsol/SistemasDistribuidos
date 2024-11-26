"""Client module for the Ice application."""
import sys
import Ice
import RemoteTypes

class Client(Ice.Application):
    """Client class for the Ice application."""

    def run(self, args):
        """Run the client application."""
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

        rdict.setItem("key1", "value1")
        rdict.setItem("key2", "value2")
        rset.add("item1")
        rset.add("item2")
        rlist.append("item1")
        rlist.append("item2")
        rlist.append("item3")
        rlist.append("item4")

        print(rdict.getItem("key1"))

        print(rlist.getItem(0))
        print(rlist.pop(0))


if __name__ == "__main__":
    app = Client()
    sys.exit(app.main(sys.argv, "client.config"))
