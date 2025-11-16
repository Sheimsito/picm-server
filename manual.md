# MANUAL DE USUARIO - PICM
## Sistema de Gestión de Inventario

---

## 1. INTRODUCCIÓN

PICM (Sistema de Gestión de Inventario) es una aplicación web diseñada para ayudar a las empresas a gestionar de manera eficiente su inventario. Este sistema permite administrar productos, categorías, insumos, proveedores y movimientos de inventario de forma centralizada y organizada.

Este manual está diseñado para guiar a los usuarios a través de todas las funcionalidades del sistema, desde el acceso inicial hasta la gestión completa de inventarios.

---

## 2. ACCESO AL SISTEMA

### 2.1 Inicio de Sesión

1. Abre la aplicación en tu navegador web.
2. En la pantalla de inicio de sesión, ingresa tus credenciales:
   - **Usuario**: Tu nombre de usuario asignado
   - **Contraseña**: Tu contraseña de acceso
3. (Opcional) Marca la casilla "Recordarme" si deseas mantener tu sesión activa.
4. Haz clic en el botón "Iniciar sesión".
5. Si las credenciales son correctas, serás redirigido automáticamente al Dashboard principal.

### 2.2 Recuperación de Contraseña

Si has olvidado tu contraseña:

1. En la pantalla de inicio de sesión, haz clic en el enlace "¿Olvidaste tu contraseña?".
2. Ingresa tu nombre de usuario o correo electrónico asociado.
3. Sigue las instrucciones que recibirás por correo electrónico para restablecer tu contraseña.

### 2.3 Cerrar Sesión

Para cerrar tu sesión de forma segura:

1. En el menú lateral izquierdo, desplázate hasta la parte inferior.
2. Haz clic en el botón "Cerrar sesión".
3. Tu sesión se cerrará y serás redirigido a la pantalla de inicio de sesión.

---

## 3. DASHBOARD PRINCIPAL

### 3.1 Descripción General

El Dashboard es la pantalla principal del sistema y proporciona una vista general de las estadísticas y métricas importantes de tu inventario. Aquí encontrarás:

- **Top 5 Productos con más Salidas**: Gráfico de barras mostrando los productos más vendidos o con más salidas en los últimos 30 días.
- **Top 5 Productos con más Entradas**: Gráfico de barras mostrando los productos con más entradas de inventario.
- **Tendencia de Movimientos por Mes**: Gráfico de líneas que muestra la evolución de entradas y salidas a lo largo del tiempo.
- **Distribución de Volumen**: Gráfico circular (dona) que muestra la proporción entre entradas y salidas.

### 3.2 Navegación

El menú lateral izquierdo te permite acceder a todas las secciones del sistema:

- **Dashboard**: Vista principal con estadísticas
- **Productos**: Gestión de productos
- **Categorías**: Organización de categorías de productos
- **Insumos**: Gestión de materias primas e insumos
- **Proveedores**: Administración de proveedores
- **Movimientos**: Registro de entradas y salidas
- **Ayuda**: Acceso al chatbot de asistencia
- **Usuario**: Configuración de tu cuenta
- **Cerrar sesión**: Salir del sistema

---

## 4. GESTIÓN DE PRODUCTOS

### 4.1 Ver Lista de Productos

1. Haz clic en "Productos" en el menú lateral.
2. Se mostrará una tabla con todos los productos registrados, incluyendo:
   - Nombre del producto
   - Descripción
   - Precio
   - Categoría a la que pertenece
   - Stock disponible
   - Botones de acción (Editar, Eliminar, Aumentar Stock, Disminuir Stock, Descargar Reporte)

### 4.2 Buscar Productos

1. En la parte superior de la tabla de productos, encontrarás un campo de búsqueda.
2. Escribe el nombre o descripción del producto que buscas.
3. La tabla se filtrará automáticamente en tiempo real mostrando solo los productos que coincidan con tu búsqueda.

### 4.3 Agregar un Producto

1. Haz clic en el botón "Agregar Producto" ubicado en la parte superior de la tabla.
2. Se abrirá un modal con un formulario. Completa los siguientes campos:
   - **Nombre**: Nombre del producto
   - **Descripción**: Descripción detallada del producto
   - **Precio**: Precio de venta del producto (número)
   - **Categoría**: Selecciona la categoría del producto del menú desplegable
3. Haz clic en el botón "Guardar" para crear el producto.
4. Verás una notificación de éxito confirmando que el producto fue creado.

### 4.4 Editar un Producto

1. En la fila del producto que deseas editar, haz clic en el botón "Editar".
2. Se abrirá un modal con el formulario prellenado con los datos actuales del producto.
3. Modifica los campos que necesites actualizar.
4. Haz clic en "Guardar" para aplicar los cambios.

### 4.5 Eliminar un Producto

1. En la fila del producto que deseas eliminar, haz clic en el botón "Eliminar".
2. Se mostrará un mensaje de confirmación para evitar eliminaciones accidentales.
3. Confirma la eliminación haciendo clic en "Aceptar" o "Confirmar".
4. El producto será eliminado permanentemente del sistema.

**Nota**: Esta acción no se puede deshacer. Asegúrate de que realmente deseas eliminar el producto.

### 4.6 Gestionar Stock de Productos

El sistema te permite aumentar o disminuir el stock de productos de forma manual:

**Aumentar Stock:**
1. Haz clic en el botón "Aumentar Stock" en la fila del producto.
2. Se abrirá un modal donde debes ingresar la cantidad a agregar.
3. Ingresa el número de unidades a aumentar.
4. Haz clic en "Guardar".

**Disminuir Stock:**
1. Haz clic en el botón "Disminuir Stock" en la fila del producto.
2. Se abrirá un modal donde debes ingresar la cantidad a reducir.
3. Ingresa el número de unidades a disminuir.
4. Haz clic en "Guardar".

### 4.7 Descargar Reporte de Producto

1. En la fila del producto, haz clic en el botón de descarga (ícono de PDF).
2. Se generará y descargará automáticamente un archivo PDF con el historial completo de movimientos del producto.

### 4.8 Paginación

Si tienes muchos productos, la tabla mostrará paginación:
- Usa los botones "Anterior" y "Siguiente" para navegar entre páginas.
- El número de página actual se muestra en el centro de los controles de paginación.

---

## 5. GESTIÓN DE CATEGORÍAS

### 5.1 Ver Lista de Categorías

1. Haz clic en "Categorías" en el menú lateral.
2. Se mostrará una tabla con todas las categorías registradas, incluyendo:
   - Nombre de la categoría
   - Descripción
   - Botones de acción (Editar, Eliminar)

### 5.2 Buscar Categorías

1. Utiliza el campo de búsqueda en la parte superior de la tabla.
2. Escribe el nombre o descripción de la categoría que buscas.
3. La tabla se filtrará automáticamente mostrando solo las categorías que coincidan.

### 5.3 Agregar una Categoría

1. Haz clic en el botón "Agregar Categoría".
2. Completa el formulario con:
   - **Nombre**: Nombre de la categoría
   - **Descripción**: Descripción de la categoría
3. Haz clic en "Guardar" para crear la categoría.

### 5.4 Editar una Categoría

1. En la fila de la categoría que deseas editar, haz clic en "Editar".
2. Modifica los campos necesarios en el formulario que se abre.
3. Haz clic en "Guardar" para aplicar los cambios.

### 5.5 Eliminar una Categoría

1. Haz clic en el botón "Eliminar" en la fila de la categoría.
2. Confirma la eliminación en el mensaje que aparece.

**Nota**: No podrás eliminar una categoría si tiene productos asociados. Primero debes eliminar o reasignar los productos de esa categoría.

---

## 6. GESTIÓN DE INSUMOS

### 6.1 Ver Lista de Insumos

1. Haz clic en "Insumos" en el menú lateral.
2. Se mostrará una tabla con todos los insumos registrados, incluyendo:
   - Nombre del insumo
   - Descripción
   - Precio Unitario
   - Proveedor Asociado
   - Stock disponible
   - Botones de acción (Editar, Eliminar, Aumentar Stock, Disminuir Stock, Descargar Reporte)

### 6.2 Buscar Insumos

1. Utiliza el campo de búsqueda en la parte superior de la tabla.
2. Escribe el nombre o descripción del insumo que buscas.
3. La tabla se filtrará automáticamente en tiempo real.

### 6.3 Agregar un Insumo

1. Haz clic en el botón "Agregar Insumo".
2. Completa el formulario con:
   - **Nombre**: Nombre del insumo
   - **Descripción**: Descripción del insumo
   - **Precio Unitario**: Precio por unidad del insumo
   - **Proveedor Asociado**: Selecciona el proveedor del menú desplegable
3. Haz clic en "Guardar" para crear el insumo.

### 6.4 Editar un Insumo

1. En la fila del insumo que deseas editar, haz clic en "Editar".
2. Modifica los campos necesarios en el formulario.
3. Haz clic en "Guardar" para aplicar los cambios.

### 6.5 Eliminar un Insumo

1. Haz clic en el botón "Eliminar" en la fila del insumo.
2. Confirma la eliminación en el mensaje de confirmación.

### 6.6 Gestionar Stock de Insumos

**Aumentar Stock:**
1. Haz clic en "Aumentar Stock" en la fila del insumo.
2. Ingresa la cantidad a agregar en el modal.
3. Haz clic en "Guardar".

**Disminuir Stock:**
1. Haz clic en "Disminuir Stock" en la fila del insumo.
2. Ingresa la cantidad a reducir en el modal.
3. Haz clic en "Guardar".

### 6.7 Descargar Reporte de Insumo

1. Haz clic en el botón de descarga (ícono de PDF) en la fila del insumo.
2. Se generará y descargará automáticamente un archivo PDF con el historial completo de movimientos del insumo.

---

## 7. GESTIÓN DE PROVEEDORES

### 7.1 Ver Lista de Proveedores

1. Haz clic en "Proveedores" en el menú lateral.
2. Se mostrará una tabla con todos los proveedores registrados, incluyendo:
   - Nombre del proveedor
   - NIT (Número de Identificación Tributaria)
   - Teléfono
   - Correo electrónico
   - Dirección
   - Botones de acción (Editar, Eliminar)

### 7.2 Buscar Proveedores

1. Utiliza el campo de búsqueda en la parte superior de la tabla.
2. Escribe cualquier dato del proveedor (nombre, NIT, correo, etc.).
3. La tabla se filtrará automáticamente mostrando solo los proveedores que coincidan.

### 7.3 Agregar un Proveedor

1. Haz clic en el botón "Agregar Proveedor".
2. Completa el formulario con:
   - **Nombre**: Nombre o razón social del proveedor
   - **NIT**: Número de Identificación Tributaria
   - **Teléfono**: Número de contacto
   - **Correo**: Dirección de correo electrónico
   - **Dirección**: Dirección física del proveedor
3. Haz clic en "Guardar" para crear el proveedor.

### 7.4 Editar un Proveedor

1. En la fila del proveedor que deseas editar, haz clic en "Editar".
2. Modifica los campos necesarios en el formulario.
   - **Nota**: El NIT no se puede editar una vez creado el proveedor.
3. Haz clic en "Guardar" para aplicar los cambios.

### 7.5 Eliminar un Proveedor

1. Haz clic en el botón "Eliminar" en la fila del proveedor.
2. Confirma la eliminación en el mensaje que aparece.

**Nota**: No podrás eliminar un proveedor si tiene insumos asociados. Primero debes eliminar o reasignar los insumos de ese proveedor.

---

## 8. GESTIÓN DE MOVIMIENTOS

### 8.1 Acceder a Movimientos

1. Haz clic en "Movimientos" en el menú lateral.
2. Se mostrará una pantalla donde debes seleccionar el tipo de movimiento:
   - **Productos**: Para ver movimientos de productos
   - **Insumos**: Para ver movimientos de insumos
3. Selecciona el tipo deseado del menú desplegable.
4. Haz clic en el botón "Consultar".

### 8.2 Ver Lista de Movimientos

Una vez seleccionado el tipo, se mostrará una tabla con todos los movimientos registrados, incluyendo:
- Producto/Insumo afectado
- Usuario que realizó el movimiento
- Tipo de Modificación (Entrada o Salida)
- Stock Modificado (cantidad)
- Comentario (si existe)
- Fecha de Creación
- Botones de acción (Editar, Eliminar)

### 8.3 Buscar Movimientos

1. Utiliza el campo de búsqueda en la parte superior de la tabla.
2. Escribe cualquier dato del movimiento (producto, usuario, fecha, etc.).
3. La tabla se filtrará automáticamente en tiempo real.

### 8.4 Agregar un Movimiento

1. Haz clic en el botón "Agregar Movimiento".
2. Completa el formulario con:
   - **Producto/Insumo**: Selecciona el producto o insumo del menú desplegable
   - **Usuario**: Selecciona el usuario que realiza el movimiento
   - **Tipo de Modificación**: Selecciona "Entrada" o "Salida"
   - **Stock Modificado**: Ingresa la cantidad de unidades
   - **Comentario**: (Opcional) Agrega un comentario sobre el movimiento
3. Haz clic en "Guardar" para registrar el movimiento.

**Nota**: El stock del producto o insumo se actualizará automáticamente según el tipo de movimiento (entrada aumenta, salida disminuye).

### 8.5 Editar un Movimiento

1. En la fila del movimiento que deseas editar, haz clic en "Editar".
2. Modifica los campos necesarios en el formulario.
3. Haz clic en "Guardar" para aplicar los cambios.

### 8.6 Eliminar un Movimiento

1. Haz clic en el botón "Eliminar" en la fila del movimiento.
2. Confirma la eliminación en el mensaje que aparece.

**Nota**: Al eliminar un movimiento, el stock se ajustará automáticamente (si era una entrada, se restará; si era una salida, se sumará).

---

## 9. SISTEMA DE AYUDA (CHATBOT)

### 9.1 Abrir el Chatbot

1. En el menú lateral, haz clic en el botón "Ayuda".
2. Se abrirá una ventana de chat en la esquina inferior derecha de la pantalla.

### 9.2 Usar el Chatbot

1. Escribe tu pregunta o consulta en el campo de texto ubicado en la parte inferior del chat.
2. Haz clic en el botón de envío (ícono de avión de papel) o presiona Enter.
3. El chatbot responderá automáticamente a tu consulta.
4. Puedes hacer múltiples preguntas en la misma sesión de chat.

### 9.3 Cerrar el Chatbot

- Haz clic nuevamente en el botón "Ayuda" en el menú lateral, o
- Haz clic fuera de la ventana del chat (en el área oscura del fondo).

---

## 10. CONFIGURACIÓN DE USUARIO

### 10.1 Ver Información del Usuario

1. En el menú lateral, haz clic en el botón "Usuario" (muestra tu nombre de usuario).
2. Se mostrará información sobre tu sesión actual.

**Nota**: La funcionalidad completa de configuración de usuario puede estar en desarrollo según la versión del sistema.

---

## 11. NOTIFICACIONES DEL SISTEMA

El sistema utiliza un sistema de notificaciones para informarte sobre el estado de las operaciones:

- **Notificaciones de Éxito** (Verde): Indican que una operación se completó correctamente.
- **Notificaciones de Error** (Rojo): Indican que ocurrió un error al realizar una operación.
- **Notificaciones de Advertencia** (Amarillo): Alertan sobre situaciones que requieren atención.
- **Notificaciones de Información** (Azul): Proporcionan información adicional.

Las notificaciones aparecen automáticamente en la esquina superior de la pantalla y desaparecen después de unos segundos.

---

## 12. CONSEJOS Y MEJORES PRÁCTICAS

1. **Búsqueda Eficiente**: Utiliza el campo de búsqueda en cada sección para encontrar rápidamente los registros que necesitas.

2. **Validación de Datos**: Asegúrate de completar todos los campos requeridos antes de guardar. Los campos obligatorios suelen estar marcados con un asterisco (*).

3. **Confirmación de Eliminación**: Siempre lee cuidadosamente los mensajes de confirmación antes de eliminar registros, ya que esta acción generalmente no se puede deshacer.

4. **Gestión de Stock**: Mantén un registro actualizado del stock. Revisa regularmente los niveles de inventario y realiza ajustes cuando sea necesario.

5. **Uso de Reportes**: Descarga los reportes PDF regularmente para mantener un respaldo de los movimientos importantes.

6. **Organización con Categorías**: Utiliza las categorías para organizar mejor tus productos y facilitar su búsqueda.

7. **Información de Proveedores**: Mantén actualizada la información de contacto de tus proveedores para facilitar la comunicación.

---

## 13. SOLUCIÓN DE PROBLEMAS

### 13.1 No puedo iniciar sesión

- Verifica que estés ingresando correctamente tu nombre de usuario y contraseña.
- Asegúrate de que la tecla Bloq Mayús no esté activada.
- Si olvidaste tu contraseña, utiliza la opción "¿Olvidaste tu contraseña?".
- Verifica que tengas conexión a internet.

### 13.2 No se cargan los datos

- Verifica tu conexión a internet.
- Intenta recargar la página presionando F5 o haciendo clic en el botón de recarga del navegador.
- Cierra sesión y vuelve a iniciar sesión.
- Si el problema persiste, contacta al administrador del sistema.

### 13.3 Error al guardar un registro

- Verifica que todos los campos requeridos estén completos.
- Asegúrate de que los valores numéricos sean válidos (números positivos, sin caracteres especiales).
- Verifica que no haya caracteres inválidos en los campos de texto.
- Intenta nuevamente después de unos segundos.

### 13.4 No puedo eliminar un registro

- Algunos registros no se pueden eliminar si tienen relaciones con otros datos (por ejemplo, una categoría con productos asociados).
- Verifica que no haya dependencias antes de intentar eliminar.
- Si es necesario, primero elimina o modifica los registros relacionados.

### 13.5 El chatbot no responde

- Verifica tu conexión a internet.
- Intenta cerrar y abrir nuevamente el chatbot.
- Recarga la página si el problema persiste.

---

## 14. GLOSARIO DE TÉRMINOS

- **Dashboard**: Panel principal del sistema que muestra estadísticas y gráficos.
- **Producto**: Artículo final que se vende o utiliza en la operación del negocio.
- **Categoría**: Clasificación utilizada para organizar productos de manera lógica.
- **Insumo**: Materia prima o material utilizado en la producción o elaboración de productos.
- **Proveedor**: Empresa o persona que suministra insumos a la organización.
- **Movimiento**: Registro de entrada o salida de productos o insumos del inventario.
- **Stock**: Cantidad disponible de un producto o insumo en el inventario.
- **Entrada**: Movimiento que aumenta el stock disponible.
- **Salida**: Movimiento que disminuye el stock disponible.
- **Reporte PDF**: Documento descargable en formato PDF que contiene información detallada sobre movimientos o registros.

---

## 15. CONTACTO Y SOPORTE

Para obtener ayuda adicional o reportar problemas:

- Utiliza el chatbot de ayuda integrado en la aplicación (botón "Ayuda" en el menú lateral).
- Contacta al administrador del sistema.
- Consulta la documentación técnica si tienes acceso a ella.

---

## FIN DEL MANUAL

Este manual cubre las funcionalidades principales del sistema PICM. Si encuentras alguna funcionalidad no documentada o tienes sugerencias para mejorar este manual, por favor contacta al equipo de soporte.

**Última actualización**: 2024

---

*Gracias por utilizar PICM - Sistema de Gestión de Inventario*

