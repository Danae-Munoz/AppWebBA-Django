from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    TIPOUSU_CHOICES = [
        ('Cliente', 'Cliente'),
        ('Técnico', 'Técnico'),
        ('Bodeguero', 'Bodeguero'),
        ('Vendedor', 'Vendedor'),
        ('Administrador', 'Administrador'),
        ('Superusuario', 'Superusuario'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(primary_key=True, max_length=20)
    tipousu = models.CharField(choices=TIPOUSU_CHOICES, max_length=50, null=False, blank=False)
    dirusu = models.CharField(max_length=300, null=False, blank=False)
    
    class Meta:
        db_table = 'PerfilUsuario'

    def __str__(self):
        return f'{self.rut} - {self.user.first_name} {self.user.last_name}'

class Producto(models.Model):
    idprod = models.IntegerField(primary_key=True, verbose_name='ID Prod')
    nomprod = models.CharField(max_length=100, null=False, blank=False, verbose_name='Nombre')
    descprod = models.CharField(max_length=300, null=False, blank=False, verbose_name='Descripción')
    precio = models.IntegerField(null=False, blank=False, verbose_name='Precio')
    imagen = models.ImageField(upload_to="images/", default="sinfoto.jpg", null=False, blank=False, verbose_name="Imagen")

    class Meta:
        db_table = 'Producto'
    
    def __str__(self):
        return f'{self.idprod} - {self.nomprod}'

class Factura(models.Model):
    nrofac = models.IntegerField(primary_key=True)
    rutcli = models.ForeignKey(PerfilUsuario, models.DO_NOTHING, db_column='rutcli', null=False, blank=False)
    idprod = models.ForeignKey(Producto, models.DO_NOTHING, db_column='idprod', null=False, blank=False)
    fechafac = models.DateField(null=False, blank=False)
    descfac = models.CharField(max_length=300, null=False, blank=False)
    monto = models.IntegerField(null=False, blank=False)

    class Meta:
        db_table = 'Factura'
    
    def __str__(self):
        clave = f'F-{self.nrofac}'
        solsers = SolicitudServicio.objects.raw(f'SELECT * FROM SolicitudServicio WHERE nrofac={self.nrofac}')
        if len(solsers) > 0:
            clave += f' SS-{solsers[0].nrosol}-{solsers[0].tiposol[:3].upper()}'
        stocks = StockProducto.objects.raw(f'SELECT * FROM StockProducto WHERE nrofac={self.nrofac}')
        if len(stocks) > 0:
            clave += f' IDS-{stocks[0].idstock}'
        else:
            clave += f' **********'
        return f'{clave} - {self.rutcli.user.first_name[0]}. {self.rutcli.user.last_name} - {self.idprod.nomprod}'

class SolicitudServicio(models.Model):
    TIPOSOL_CHOICES = [
        ('Instalación', 'Instalación'),
        ('Mantención', 'Mantención'),
        ('Reparación', 'Reparación'),
    ]
    ESTADOSOL_CHOICES = [
        ('Aceptada', 'Aceptada'),
        ('Modificada', 'Modificada'),
        ('Cerrada', 'Cerrada'),
        ('Anulada', 'Anulada'),
    ]
    nrosol = models.IntegerField(primary_key=True)
    nrofac = models.ForeignKey(Factura, models.DO_NOTHING, db_column='nrofac', null=False, blank=False)
    tiposol = models.CharField(choices=TIPOSOL_CHOICES, max_length=50, null=False, blank=False)
    fechavisita = models.DateField(null=False, blank=False)
    ruttec = models.ForeignKey(PerfilUsuario, models.DO_NOTHING, db_column='ruttec', null=False, blank=False)
    descsol = models.CharField(max_length=200, null=False, blank=False)
    estadosol = models.CharField(choices=ESTADOSOL_CHOICES, max_length=50, null=False, blank=False)

    class Meta:
        db_table = 'SolicitudServicio'
    
    def __str__(self):
        clave = f'{self.nrosol} - {self.tiposol} - Técnico ({self.ruttec.user.first_name} {self.ruttec.user.last_name})'
        clave += f' - Cliente ({self.nrofac.rutcli.user.first_name} {self.nrofac.rutcli.user.last_name}) Factura ({self.nrofac})'
        return clave

class GuiaDespacho(models.Model):
    ESTADOGD_CHOICES = [
        ('En bodega', 'En bodega'),
        ('Despachado', 'Despachado'),
        ('Entregado', 'Entregado'),
    ]
    nrogd = models.IntegerField(primary_key=True)
    nrofac = models.ForeignKey(Factura, models.DO_NOTHING, db_column='nrofac', null=False, blank=False)
    idprod = models.ForeignKey(Producto, models.DO_NOTHING, db_column='idprod', null=False, blank=False)
    estadogd = models.CharField(choices=ESTADOGD_CHOICES, max_length=50, null=False, blank=False)

    class Meta:
        db_table = 'GuiaDespacho'

    def __str__(self):
        clave = f'{self.nrogd} - Cliente ({self.nrofac.rutcli.user.first_name} {self.nrofac.rutcli.user.last_name})'
        clave += f' -  Factura ({self.nrofac}, {self.nrofac.idprod.nomprod})'
        return clave

class StockProducto(models.Model):
    idstock = models.IntegerField(primary_key=True)
    idprod = models.ForeignKey(Producto, models.DO_NOTHING, db_column='idprod', null=False, blank=False)
    nrofac = models.ForeignKey(Factura, models.DO_NOTHING, db_column='nrofac', blank=True, null=True)

    class Meta:
        db_table = 'StockProducto'
    
    def __str__(self):
        clave = ''
        if self.nrofac is not None:
            cliente = f'Cliente ({self.nrofac.rutcli.user.first_name} {self.nrofac.rutcli.user.last_name})'
            factura = f'Factura ({self.nrofac}, {self.nrofac.idprod.nomprod})'
            clave = f'{self.idstock} - {cliente} - {factura}'
        else:
            clave = f'{self.idstock} - Producto en bodega'
        return clave

class AnwoStockProducto(models.Model):
    RESERVADO_CHOICES = [
        ('S', 'Reservado'),
        ('N', 'No reservado'),
    ]
    nroserieanwo = models.CharField(primary_key=True, max_length=100)
    nomprodanwo = models.CharField(max_length=100, null=False, blank=False)
    precioanwo = models.IntegerField(null=False, blank=False)
    reservado = models.CharField(choices=RESERVADO_CHOICES, max_length=1, null=False, blank=False)

    class Meta:
        db_table = 'AnwoStockProducto'
        
    def __str__(self):
        return f'{self.nroserieanwo} - {self.nomprodanwo}'