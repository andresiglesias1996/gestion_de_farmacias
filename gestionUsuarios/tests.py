from django.test import TestCase
from gestionStock.models import Farmacias

# Create your tests here.
class UsuarioTest(TestCase):

    def setUp(self):
        #Setup run before every test method.
        print("ejecuta setUp()")
        nuevoFarmacia = Farmacias.objects.create(nombre="farmacia coso",direccion="la calle", localidad="la locali", departamento="Canelones")
        nuevoFarmacia.save()
        pass

    def tearDown(self):
            #Clean up run after every test method.
        print("ejecuta tearDown()")

        pass

    def test_something_that_will_pass(self):
        nuevoFarmacia = Farmacias.objects.create(nombre="farmacia coso",direccion="la calle", localidad="la locali", departamento="Canelones")
        nuevoFarmacia.save()
        self.assertFalse(False)

    def test_something_that_will_fail(self):
        nuevoFarmacia = Farmacias.objects.create(nombre="farmacia coso",direccion="la calle", localidad="la locali", departamento="Canelones")
        nuevoFarmacia.save()
        self.assertTrue(False)
