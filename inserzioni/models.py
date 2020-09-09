from django.db import models
from django.http import HttpResponse
from django.urls import reverse
from django.template.defaultfilters import slugify
from utenti.models import Profile


class Categoria(models.Model):
    nome = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True ,db_index=True)
    orario_creazione = models.DateTimeField(auto_now_add=True)
    orario_aggiornamento = models.DateTimeField(auto_now=True)
 
    class Meta:
        ordering = ('nome', )
        verbose_name = 'catergoria'
        verbose_name_plural = 'categorie'
 
    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('inserzioni:lista_prodotti_filtro_regione_categoria', args=["all",self.slug])
		
		
		
		
class Regione(models.Model):
    nome = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True ,db_index=True)
    orario_creazione = models.DateTimeField(auto_now_add=True)
    orario_aggiornamento = models.DateTimeField(auto_now=True)
 
    class Meta:
        ordering = ('nome', )
        verbose_name = 'regione'
        verbose_name_plural = 'regioni'
 
    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('inserzioni:lista_prodotti_filtro_regione_categoria', args=[self.slug, "all"])
 
 
class Prodotto(models.Model):
	categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
	regione = models.ForeignKey(Regione, on_delete=models.CASCADE)
	user = models.ForeignKey(Profile, on_delete=models.CASCADE)
	nome = models.CharField(max_length=200, db_index=True)
	slug = models.SlugField(max_length=200, db_index=True)
	descrizione = models.TextField(blank=True)
	prezzo = models.DecimalField(max_digits=10, decimal_places=2)
	disponibilita = models.BooleanField(default=True)
	venduto = models.BooleanField(default=False)
	orario_creazione = models.DateTimeField(auto_now_add=True)
	orario_aggiornamento = models.DateTimeField(auto_now=True)
	immagine = models.ImageField(upload_to='media/%Y/%m/%d', blank=True)
 
	class Meta:
		ordering = ('-orario_creazione', )
		verbose_name = 'prodotto'
		verbose_name_plural = 'prodotti'
		index_together = (('id', 'slug'),)

	def __str__(self):
		return self.nome
		
	def save(self, *args, **kwargs):
		self.slug = slugify(self.nome)
		super(Prodotto, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('inserzioni:dettaglio_prodotti', args=[self.id, self.slug])
		
	def get_absolute_url_for_my_list(self):
		return reverse('inserzioni:modifica_prodotti', args=[self.id, self.slug])