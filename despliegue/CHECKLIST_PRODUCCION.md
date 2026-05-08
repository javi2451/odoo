# Checklist: Configuración Manual Inicial en Producción (Base Limpia)

Cuando instales Odoo en Google Cloud **sin datos de demostración**, al entrar por primera vez deberás seguir esta ruta exacta para dejar todo el entorno funcional de la carnicería listo para tu capacitación. 

Sigue el orden de forma estricta:

## FASE 1: Configuración General (La Base)
- [ ] **Instalar la Plantilla:** Ve a Aplicaciones y dale instalar a "Plantilla para Carnicería" (esto forzará la instalación de todo lo demás como Inventario, Punto de Venta, etc.).
- [ ] **Configurar Moneda:** Ve a *Ajustes > Ajustes Generales* y cambia la moneda principal a **PEN (Soles Peruanos)**.
- [ ] **Configurar Idioma:** En esos mismos ajustes generales, carga el idioma **Spanish (Español)** y establécelo para tu usuario Admin.
- [ ] **Datos de la Compañía:** En *Ajustes > Empresas*, edita "My Company" y pon el logo real de la carnicería, RUC (Tax ID), dirección y nombre. Esto es lo que saldrá impreso en todos los tickets.

## FASE 2: Activar el "Poder" del Inventario
- [ ] **Activar Kilos (UoM):** Ve a *Ajustes > Inventario* > Marca la casilla de **"Unidades de Medida"**. Es sumamente obligatorio hacerlo antes de crear el primer producto.
- [ ] **Activar Multilocales:** En la misma pantalla de Ajustes de Inventario, marca la opción de **"Ubicaciones de Almacenamiento"** (Storage Locations) y **"Almacenes Múltiples"** (Multi-Warehouses). Guarda los cambios.

## FASE 3: Crear la Estructura Física
- [ ] **Crear los Almacenes:** Ve a *Inventario > Configuración > Almacenes*. Odoo ya creó el central (My Company). Haz clic en Nuevo y crea los demás físicamente (Ej: Local Sur, Local Norte, etc.). Deja que Odoo genere las ubicaciones solo.

## FASE 4: Los Métodos de Pago y el Dinero
- [ ] **Diarios de Efectivo:** Ve a *Contabilidad/Facturación > Configuración > Diarios* (o desde el mismo Punto de Venta al crear el método de pago). Crea diarios tipo Efectivo INDEPENDIENTES para cada local físico (Ej: `Caja Local Central`, `Caja Fija Sur`).
- [ ] **Métodos de Pago del PdV:** Entra al módulo de Punto de Venta. Crea los métodos de pago asignando cada Diario de efectivo a su local. Puedes crear un único método llamado "Tarjeta Vinculada" o "POS Visa" (de tipo Banco) que pueda ser compartido por todos.

## FASE 5: Crear los 5 Puntos de Venta (Mostradores)
- [ ] **Cajas por Local:** Ve a *Punto de Venta > Configuración > Puntos de venta*. Crea las 5 "Tiendas". 
- [ ] **Conexión de Inventario (Crucial):** Entra a los ajustes de cada Punto de Venta que acabas de crear. Ve a la parte de Inventario > "Tipo de Operación" y asígnale el "POS Orders" correcto que coincida con su almacén físico (Ej: La caja del Sur extrae del almacén del Sur).
- [ ] **Conexión de Dinero:** En esos mismos ajustes, asígnales a cada caja el Método de Pago "Efectivo" independiente que creaste en la Fase 4.

## FASE 6: Restricción de Usuarios
- [ ] **Crear Empleados/Cajeros:** Por último, ve a *Ajustes > Administrar Usuarios*. Crea los 5 correos para los cajeros. 
- [ ] **Permisos de Cajero:** Deja todo absolutamente en blanco, excepto la sección Punto de Venta donde debe decir `Usuario`.
- [ ] **Contraseñas:** Guárdalos y entra arriba a *Acción > Cambiar Contraseña* para asignar manualmente las claves de ingreso de tus empleados (`1234` etc.), como aprendiste a "forzar" la confirmación de sistema.

---
> Si dejas esto hecho, cuando llegue el cliente a la capacitación solo tendrás que enseñarle a crear 1 carne en kilos, mostrarle la pantalla de manufactura para su Vaca y cómo abrir la caja a vender. Todo el entramado financiero e inventario complejo ya estará trabajando en silencio detrás de cámaras.
