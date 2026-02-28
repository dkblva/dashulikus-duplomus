using Microsoft.EntityFrameworkCore;
using FormApi.Data;
using FormApi.Models;

var builder = WebApplication.CreateBuilder(args);


builder.Services.AddDbContext<ApplicationContext>(options =>
    options.UseSqlServer(
        "Server=(LocalDB)\\MSSQLLocalDB;Database=FormDB;Trusted_Connection=True;TrustServerCertificate=True;"
    ));


// ✅ Подключаем контроллеры
builder.Services.AddControllers();

// ✅ CORS (чтобы сайт мог обращаться к API)
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll", policy =>
        policy.AllowAnyOrigin()
              .AllowAnyHeader()
              .AllowAnyMethod());
});

var app = builder.Build();

// ❗ Отключаем принудительный HTTPS (у тебя его нет)
app.UseHttpsRedirection();

// ✅ Включаем CORS
app.UseCors("AllowAll");

// ✅ Подключаем маршруты контроллеров
app.MapControllers();

app.Run();
