using Microsoft.EntityFrameworkCore;
using FormApi.Data;
using FormApi.Models;

var builder = WebApplication.CreateBuilder(args);


builder.Services.AddDbContext<ApplicationContext>(options =>
    options.UseSqlServer(
        "Server=KOMPUTER;Database=FormDB;Trusted_Connection=True;TrustServerCertificate=True;"
    ));


// ✅ Подключаем контроллеры
builder.Services.AddControllers();

// ✅ Swagger/OpenAPI (Swashbuckle)
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

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

// ✅ Swagger middleware
if (app.Environment.IsDevelopment() || app.Environment.IsStaging())
{
    app.UseSwagger();
    app.UseSwaggerUI(options =>
    {
        options.SwaggerEndpoint("/swagger/v1/swagger.json", "FormApi v1");
        options.RoutePrefix = string.Empty; // serve at root if desired
    });
}

// ✅ Подключаем маршруты контроллеров
app.MapControllers();

app.Run();
