# Arquitectura de ExploraNica

ExploraNica utiliza .NET 10, Windows Forms, ASP.NET Core, Entity Framework Core y PostgreSQL. El sistema se organiza en dominio, aplicación, infraestructura y presentación.

| Componente | Ubicación en el repositorio del sistema |
| --- | --- |
| Entidades y estados | `src/Core/ExploraNica.Domain` |
| DTO, contratos y validadores | `src/Core/ExploraNica.Application` |
| Persistencia, migraciones y servicios | `src/Infrastructure/ExploraNica.Infrastructure` |
| Configuración y utilidades de interfaz | `src/Infrastructure/ExploraNica.Shared` |
| API | `src/Presentation/ExploraNica.Api` |
| Cliente del operador | `src/Presentation/ExploraNica.OperatorApp` |
| Cliente administrativo | `src/Presentation/ExploraNica.AdminApp` |

El repositorio oficial es https://github.com/AJcano09/explora-nicaragua.

La API centraliza autenticación, gestión de operadores, documentos, tours, sesiones, reservas y validación de vouchers. Los clientes intercambian JSON con el servidor. PostgreSQL conserva las entidades y el servicio de almacenamiento gestiona los archivos documentales.
