
# estas son las líneas que producen el resultado
txt_index = "Tu índice de Ruffier: "
txt_workheart = "Eficiencia del corazón: "
txt_nodata = '''
no hay datos para edad'''
txt_res = []
txt_res.append('''bajo.
¡Visita a tu doctor de inmediato!''')
txt_res.append('''satisfactory.
¡Visita a tu doctor de inmediato!''')
txt_res.append('''promedio.
Tal vez valga la pena hacerse unas pruebas adicionales con el doctor.''')
txt_res.append('''
más alto que el promedio''')
txt_res.append('''
alto''')
 
def ruffier_index(P1, P2, P3):
   ''' Retorna el valor del índice según los tres cálculos de pulso para su comparación con la tabla'''
   return (4 * (P1+P2+P3) - 200) / 10
 
def neud_level(age):
   ''' las opciones con una edad menor que 7 y con adultos deben ser procesadas por separado,
   aquí seleccionamos el nivel “insatisfactorio” solo dentro de la tabla:
   para la edad de 7, “insatisfactorio” es un índice de 21, luego en adelante cada 2 años disminuye en 1.5 hasta el nivel de 15 a los 15-16 años '''
   norm_age = (min(age, 15) - 7) // 2  # cada dos años desde los siete años se convierte en una unidad, hasta los 15 años
   result = 21 - norm_age * 1.5 # cada dos años se multiplica la diferencia por 1.5, así son organizados los niveles en la tabla
   return result
  
def ruffier_result(r_index, level):
   ''' la función obtiene el índice de Ruffier y lo interpreta, retornamos el nivel de preparación: un número del 0 al 4 (mientras más alto el nivel de preparación, mejor).  '''
   if r_index >= level:
       return 0
   level = level - 4 # esto no se ejecutará si ya se retornó la respuesta “insatisfactorio”
   if r_index >= level:
       return 1
   level = level - 5 # de manera análoga, terminamos aquí si el nivel es, como mínimo, “satisfactorio”
   if r_index >= level:
       return 2
   level = level - 5.5 # siguiente nivel
   if r_index >= level:
       return 3
   return 4 # terminamos aquí si el índice es menor que todos los niveles intermedios, es decir, el círculo probado.
 
def test(P1, P2, P3, age):
   ''' esta función puede ser usada desde afuera del módulo para calcular el índice de Ruffier.
   Retornamos los textos listos que solo necesitan ser escritos en el lugar necesario
   Usamos las constantes usadas al inicio del módulo para textos. '''
   if age < 7:
       return (txt_index + "0", txt_nodata) # Esto es un misterio más allá de esta prueba
   else:
       ruff_index = ruffier_index(P1, P2, P3) # cálculo
       result = txt_res[ruffier_result(ruff_index, neud_level(age))] # la interpretación y conversión del nivel de preparación numérica a dato de texto
       res = txt_index + str(ruff_index) + '\n' + txt_workheart + result
       return res