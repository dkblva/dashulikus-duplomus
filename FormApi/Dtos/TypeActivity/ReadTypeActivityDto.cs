using System;

namespace FormApi.Dtos.TypeActivity
{
    public class ReadTypeActivityDto
    {
        public Guid Id { get; set; }
        public string NameType { get; set; } = null!;
    }
}