using System;

namespace FormApi.Dtos.SphereActivity
{
    public class ReadSphereActivityDto
    {
        public Guid Id { get; set; }
        public string NameSphere { get; set; } = null!;
    }
}