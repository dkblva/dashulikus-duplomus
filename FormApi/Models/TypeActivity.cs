using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace FormApi.Models
{
    public class TypeActivity //вид деятельности организации
    {
        public Guid Id { get; set; } // код вида деятельности

        public string NameType { get; set; } //наименование
    }
}
