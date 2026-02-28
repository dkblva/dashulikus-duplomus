using Microsoft.EntityFrameworkCore;
using FormApi.Models;

namespace FormApi.Data;

public class ApplicationContext : DbContext
{
    public DbSet<Application> Applications { get; set; } = null!;

    public DbSet<Tarif> Tarifs { get; set; } = null!;

    public DbSet<FormData> FormDatas { get; set; } = null!;

    public DbSet<SphereActivity> SphereActivities { get; set; } = null!;

    public DbSet<TypeActivity> TypeActivities { get; set; } = null!;

    public DbSet<Solution> Solutions { get; set; } = null!;




    public ApplicationContext(DbContextOptions<ApplicationContext> options)
        : base(options)
    {
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);
    }
}


