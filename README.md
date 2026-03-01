# UpsideRolls: StrangerRPG Documentación

## Descripción breve del proyecto

## Instalación
**No usar ninguna de las credenciales de ejemplo**


### Paso 1 - Revisar la instalación de Docker en tu sistema
```
docker --version
docker compose version
```

### Paso 2 - Creamos un archivo .env para nuestras variables de entorno

```
POSTGRES_DB=db_ejemplo
POSTGRES_USER=usuario_ejemplo
POSTGRES_PASSWORD=1234

DB_NAME=db_ejemplo
DB_USER=usuario_ejemplo
DB_PASSWORD=1234
DB_HOST=db
DB_PORT=5432
SECRET_KEY=clave_secreta
DEBUG=True
```


### Paso 4 - Construir y levantar los contenedores
```
docker compose up --build -d
```

### Paso 5 - Acceder a la aplicación
```
http://localhost:8000
```

### Dependencias

## Vamos, pruebalo por ti mismo!

Ya que te has interesado lo suficiente como para llegar hasta aquí vamos a hacer una pequeña guía para que entiendas cómo funciona la aplicación.

Primero, al ingresar al enlace desde tu navegador, encontrarás la pantalla de inicio de sesión.

![inicio-login](docs/img/inicio-login.png)

Seguramente ya estás familiarizado con esta dinámica.
Si ya tienes una cuenta, simplemente inicia sesión con tus datos.
Si no la tienes, haz clic en **“Registro”** (arriba a la derecha) o en **“Regístrate”** justo debajo del botón de **“Entrar”**.

Supongamos que somos completamente nuevos.

![registro](docs/img/registro.png)

Procedemos a rellenar los campos que nos solicita el formulario y pulsamos en **“Unirse”**.

¡Y ya estaría! Ya tenemos la cuenta creada. La aplicación nos redirigirá directamente a nuestra página principal.

![no-campana](docs/img/no-campana.png)

Aquí veremos que todavía no tenemos ninguna campaña creada, así que, ¿a qué esperamos? ¡Vamos a crear una!

Rellenamos ...

![campana-creacion](docs/img/campana-creacion.png)

Ahora que ya la tenemos creada, podemos ir a la Batalla, así que hacemos clic ahí.

![campana-no-pj](docs/img/campana-no-pj.png)

Oh, espera. No tenemos ningún personaje ni ningún enemigo creado para nuestro juego.

Vamos a volver al menú para solucionarlo.

Hacemos clic en **Nuevo Personaje** y aparecerá la pantalla de creación.

Rellenamos los campos. POdemos elegir entre diferentes opciones, como la vida, la clase, etc.

![Personaje-Ejemplo](docs/img/Personaje-Ejemplo.png)

Con nuestro personaje listo, ahora sí, vamos a crear el enemigo.

Rellenamos los campos y lo creamos.

![Enemigo-Ejemplo](docs/img/Enemigo-Ejemplo.png)

¡Ahora sí que sí! Vamos a la batalla.

La dinámica es sencilla.

Lo primero que debemos saber es que tenemos dos tipos de acción:
- Curarnos a nosotros mismos.
- Atacar al enemigo.

Si decidimos atacar, podremos:
- Seleccionar el enemigo que queramos.
- Elegir qué tipo de dados usar.
- Escoger el modificador.

![atarcar-enemigo](docs/img/atarcar-enemigo.png)

Al hacer clic en **Ejecutar**, los dados se lanzarán y determinarán el daño que hacemos al enemigo.
El turno del enemigo se ejecutará al mismo tiempo que el nuestro.

Si optamos por curarnos, podremos recuperar vida según el resultado de los dados.
Eso si, el enemigo también podrá atacarnos durante esa misma tirada.

![curarse](docs/img/curarse.png)

En la parte inferior de la pantalla tenemos el **historial de combate**, donde quedará registrado todo lo que ha sucedido durante nuestra campaña.

![historial-combate](docs/img/historial-combate.png)

Cuando derrotamos a todos los enemigos, recibiremos una pantalla indicando que han sido eliminados, marcando así el final de la campaña.

![victoria](docs/img/victoria.png)

Y hasta aquí la guía.Espero que te haya gustado y que disfrutes tu aventura.



## Estructura del proyecto

## Documentación del codigo

### Aplicación ``` accounts ```

#### Usuario personalizado ```models.py```

Se implementa un modelo ```CustomUser``` extendiendo ```Abstractuser``` 

Elegimos este enfoque en vez de AbstractBaseUser porque:

```
Preguntar Luis
```

- **Email único** 

    El campo ```email``` se redifine como único y obligatorio.
    Esto permite:
    - Evitar duplicidades
    - Garantizar identificadores de contactos válidos

**Gestión de roles mediante grupos**

En lugar de crear un campo “rol” manual en el modelo, se utilizan los grupos de Django:

- Grupo DM
- Grupo PLAYER

Esto permite:
- Integrarse con el sistema de permisos nativo.
- Mantener coherencia con la arquitectura de Django.
- Facilitar la escalabilidad (posibles nuevos roles).

```
Preguntar Luis
```
#### Personalización del panel de administración  ```admin.py```

Se ha personalizado el panel de administración de Django para el modelo ```CustomUser``` mediante la extensión de ```UserAdmin```.

El objetivo  de esta configuración es:
- Facilitar la gestión de usuarios y roles.
- Mejorar la visualización de información relevante.

#### Visualización optimizada
Se definen los siguientes elementos:
- ```list_display```: muestra username, email y estado del usuario.
- ```search_fields```: permite búsqueda rápida por nombre o email.
- ```list_filter```: habilita filtrado por estado, permisos, grupos y fechas.
- ```ordering```: orden alfabético por nombre de usuario.
- ```list_per_page```: limita la paginación para mejorar legibilidad.

Los campos se agrupan las siguientes secciones:
- Información personal
- Permisos
- Fechas importantes

#### Creación de usuarios

Se define un ```add_fieldsets``` personalizado para simplificar la creación de nuevos usuarios desde el panel administrativo.

#### Formulario de registro ```forms.py```

Para la creación de nuevos usuarios se implementa un formulario personalizado basado en ```UserCreationForm```.

Se extiende ```UserCreationForm``` en lugar de crear un formulario desde cero porque incluye validaciones seguras de contraseñas y reduce complejidad y posibles errores de seguridad.
- El campo ```email``` se redefine como obligatorio en el formulario.

#### Vistas de registro y login `views.py`

`def registro(request)`

**Función:** Gestiona el registro de nuevos usuarios.

**Parámetros:**

- `request`: HttpRequest con datos del formulario.

**Devuelve:** Formulario renderizado o redirección tras registro exitoso.


`def login_view(request)`

**Función:** Autentica usuarios existentes.

**Parámetros:**
- `request`: HttpRequest con credenciales.

**Devuelve:** Formulario de login o redirección.


`def logout_view(request)`

**Función:** Cierra la sesión activa.

**Parámetros:**

- `request`: HttpRequest actual.

**Devuelve:** Redirección a la vista de autenticación.

#### `crear_grupos.py`

## Aplicación `game`

### Modelado del dominio RPG `models.py`

#### Perfil de jugador `PerfilJugador`

Se implementa un modelo `PerfilJugador` vinculado mediante relación OneToOne con el usuario. Permite acceso directo desde `user.perfil_jugador`

Este enfoque permite extender la información del usuario sin modificar el modelo de autenticación.

Con esto conseguimos 
- Separar datos de autenticación de datos de juego pa
- Mantener modularidad y escalabilidad.


#### Gestión de campañas `Campaña`

Representa una partida dirigida por un DM, con varios estados y formada por múltiples jugadores.
- El control de estado se e define un campo `estado` con `choices`:
    - activa
    - pausada
    - finalizada

Esta relacionado con:
- **DM (director)**
  - `ForeignKey` al usuario.
  - `on_delete=PROTECT`: impide eliminar un DM con campañas activas.

- **Jugador**
  - `ManyToManyField` con usuario.
  - Permite múltiples jugadores por campaña.

#### Personajes `Personaje`

Es una entidad jugable asociada a un usuario dentro de una campaña.

Se relacionad de la siguiente forma:
- `propietario` > Usuario (`CASCADE`)
- `campana` > Campaña (`CASCADE`)

Si se elimina la campaña o el usuario, el personaje desaparece automáticamente.

Le introducimos una restricción de unicidad a traves de  ```unique_together = ('nombre', 'campana')```
Evita personajes duplicados dentro de la misma campaña.

Validamos mediante el método `clean()` que:
- `vida_actual` no supere `vida_maxima`.


#### Enemigos `Enemigo`

Entidad enemiga que está asociada a una campaña.

Su relación es:
- `ForeignKey` a campaña (`CASCADE`).

Al igual que con `Personaje`, tiene restricción de unicidad: `unique_together = ('nombre', 'campana')`


#### Registro de acciones `RegistroAccion`

Modelo encargado de almacenar el historial de acciones realizadas en una campaña.

Es el núcleo dinámico del sistema.

En sus relaciones podemos observar una diferencia clave entre ellas:
- `campana` es obligatoria
- `usuario`, `personaje`, `enemigo` son opcionales (`SET_NULL`). Esto permite conservar el historial incluso si se eliminan entidades relacionadas

 Control de tipos mediante `choices`
- `TIPOS_ACCION`
- `TIPO_DADO_CHOICES`

Se incorporan campos derivados como `total`, `exito`, `dano_curacion`, etc. Sirven almacenar el resultados en las acciones, facilitando la trazabilidad.


### Personalización del panel de administración `admin.py`

Aqui se configura el panel de administración para facilitar la gestión interna de campañas, personajes y acciones del sistema RPG.

**`PerfilJugadorAdmin`**

- `list_display` y `search_fields` configurados para permitir búsqueda por nombre de usuario mediante lookup relacional (`usuario__username`).

**`CampanaAdmin`**

- Configuración estándar de listado, filtros y búsqueda.
- `filter_horizontal` aplicado al `ManyToManyField` de jugadores para mejorar la gestión visual.
- `readonly_fields` en `fecha_creacion` para preservar integridad del dato automático.


**`PersonajeAdmin`**

- Configuración estandar de listado y filtros.
- `list_editable = ['vida_actual']` permite modificar puntos de vida directamente desde la vista de lista.


**`EnemigoAdmin`**

Tiene configuración estándar orientada a filtrado por campaña, tipo y dificultad.

**`RegistroAccionAdmin`**

- Configuración de listado y filtros enfocada a análisis.
- `date_hierarchy = 'fecha'` permite navegación cronológica por registros.

Se prioriza la consulta histórica y segmentación temporal.

**`RegistroAccionInline`**
- Orden descendente por fecha.
- `extra = 0` para evitar formularios vacíos innecesarios.

Permite consultar acciones relacionadas sin abandonar el modelo principal.


### Formularios avanzados `forms.py`


`PerfilJugadorForm`
Asociado al modelo `PerfilJugador`, impide la creación de perfiles asociados a terceros.
- Se recibe el usuario por parámetro `user`.
- `clean_usuario()` garantiza que el perfil siempre esté vinculado al usuario autenticado.

`CampanaForm`

Formulario para creación y edición de campañas.
- El usuario autenticado se asigna como `dm` automáticamente.
- `clean_dm()` impide que un usuario se asigne como DM distinto.
- `clean()` impide editar campañas dirigidas por otro DM.

`PersonajeForm`

Formulario para la creación de personaje
- `clean_vida_actual()` garantiza que la vida actual no supere vida máxima.
- `clean_nivel()` garantiza que el nivel esté restringido entre 1 y 20.
- `clean()` garantiza que solo pueda crearse personaje en campañas donde el usuario participa y la valida unicidad de nombre dentro de la campaña (refuerzo adicional a `unique_together`).

`EnemigoForm`

Formulario de creación de enemigos vinculado a una campaña concreta.
- La campaña se recibe por parámetro y se oculta.
- Validación de unicidad de nombre dentro de la campaña.


`RegistroAccionForm`

Este formulario adapta su comportamiento según el usuario y la campaña

- Si el usuario pertenece al grupo **DM**, puede seleccionar enemigos.
- Si es **PLAYER**, debe seleccionar personaje obligatorio.
- `clean_campana()` Valida que el usuario pueda registrar acciones en esa campaña.
- `clean()` Principialmente verifica que exista campaña. Comprueba que personaje/enemigo pertenezcan a la campaña y que el resultado del dado esté dentro del rango permitido 


### `mixins.py`

`class SoloPropietarioMixin(UserPassesTestMixin)`

**Función:** Permite acceso solo al propietario del objeto.

- `test_func()` comprueba que `obj.propietario == request.user`.
- Si no se cumple, lanza `PermissionDenied`.

`SoloDMMixin(UserPassesTestMixin)`

**Función:** Restringe el acceso únicamente al Director de la campaña.

- `test_func()` verifica que el usuario sea el `dm`.
- Se usa para acciones exclusivas del director.


### Vistas de game `views.py`

`class CampanaView`

**Función:** Muestra la campaña activa.

- `get_context_data()` Añadimos la campaña actual al contexto del template.

**Devuelve:** Template con la campaña activa.

`class CampanaCreateView`

**Función:** Crea una nueva campaña.

- `dispatch()` Esto impìde crear más de una campaña antes de procesar la petición.
- `get_success_url()` Define la redirección tras creación exitosa.

**Devuelve:** Formulario o redirección.

`class CampanaUpdateView`

**Función:** Edita la campaña activa (solo DM).

- `get_object()` Siempre devuelve la primera campaña existente.
- `get_success_url()` Define redirección tras actualización.

**Devuelve:** Formulario o redirección.

`class CampanaDeleteView`

**Función:** Elimina la campaña activa (solo DM).

- Se implementa `get_object()` y `get_success_url()` 

**Devuelve:** Confirmación o redirección.

`class PersonajeListView`

**Función:** Lista personajes de la campaña activa.

- `get_queryset()` → Filtra personajes según la campaña actual.

**Devuelve:** Listado de personajes.

`class PersonajeCreateView`

**Función:** Crea un personaje asociado al usuario y a la campaña.

- Aqui tambien se implementa`dispatch()` y `get_success_url()`
- `form_valid()` → Asigna automáticamente propietario y campaña antes de guardar.

**Devuelve:** Formulario o redirección.

`class PersonajeUpdateView`

**Función:** Edita un personaje (solo propietario).

- Se implementa `get_success_url()`

**Devuelve:** Formulario o redirección.

`class PersonajeDeleteView`

**Función:** Elimina un personaje (solo propietario).

* `success_url` definido directamente (no sobrescribe método).

**Devuelve:** Confirmación o redirección.


`class EnemigoListView`

**Función:** Lista enemigos de la campaña (solo DM).

- `get_queryset()` Filtra enemigos según campaña activa.

**Devuelve:** Listado de enemigos.

`class EnemigoCreateView`

**Función:** Crea enemigo asociado a la campaña.

- `get_form_kwargs()` Inyecta la campaña al formulario.
- `get_success_url()` 

**Devuelve:** Formulario o redirección.

`class EnemigoUpdateView`

**Función:** Edita enemigo (solo DM).

- `get_form_kwargs()` Reinyecta la campaña.
- `get_success_url()`

**Devuelve:** Formulario o redirección.

`class EnemigoDeleteView`

**Función:** Elimina enemigo (solo DM).

- `success_url` definido directamente.

**Devuelve:** Confirmación o redirección.

`def batalla_view(request)`

**Función:** Gestiona la lógica del combate por turnos.

- Controla estado de batalla (activa, victoria, derrota).
- Gestiona turnos de enemigos y personajes.
- Genera tiradas aleatorias.
- Aplica daño o curación.
- Registra acciones en historial.
- Actualiza estado de turno en campaña.

**Devuelve:** Vista de batalla, victoria, derrota o redirección tras acción.

### ORM

**`StatsCampanaView`**

Vista basada en `TemplateView` que genera estadísticas completas de una campaña usando agregaciones y anotaciones avanzadas del ORM.



Para optimizar las consultas se utilizan:
- `select_related('dm')` evita consultas extra para el director.
- `prefetch_related(...)` precarga jugadores, personajes y registros.

Esto ayuda a que se reduzca el número de queries y optimice el rendimiento.


**Estadísticas por personaje con `annotate`**

Cada personaje de la campaña incluye:

- `total_acciones`: número total de acciones. Se usa `Count`
- `dano_total`: suma de daño en ataques. Se usa `Sum`
- `curacion_total`:  suma de curación. Se usa `Sum`

Se filtran las condiciones con `Q`

Esto genera métricas individuales por personaje.


**Estadísticas globales con `aggregate`**

Sobre todos los registros de la campaña:

- Total de acciones. `Count`
- Media de tiradas. `Avg`
- Daño máximo registrado. `Sum`
- Daño total. `Sum`
- Curación total. `Sum`


A la hora de filtrar, se construye una queryset que:
- Filtra solo ataques y curaciones.
- Solo acciones exitosas.
- Permite búsqueda opcional por nombre (personaje o enemigo).
- Usa `select_related`, lo cual optimiza relaciones.



#### `def aplicar_dano`

**Función:** Aplica daño a un personaje reduciendo su vida actual directamente en base de datos.

**Parámetros:**

- `request`: HttpRequest con el valor de daño enviado por POST.
- `pk`: Identificador del personaje afectado.

**Devuelve:** Redirección a la vista de detalle del personaje tras actualizar la vida.

Solo permite modificar personajes cuyo propietario sea el usuario autenticado.





