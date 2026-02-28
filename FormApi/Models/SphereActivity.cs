using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace FormApi.Models
{
    public class SphereActivity //сфера деятельности предприятия 
    {
        public Guid Id { get; set; } //код сферы деятельности

        public string NameSphere { get; set; } //наименование
    }
}
