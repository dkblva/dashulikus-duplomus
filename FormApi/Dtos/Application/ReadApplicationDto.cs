using System;

namespace FormApi.Dtos.Application
{
    public class ReadApplicationDto
    {
        public Guid Id { get; set; }
        public string FullName { get; set; } = null!;
        public string? PhoneNumber { get; set; }
        public string? Email { get; set; }
        public string? OrganizationName { get; set; }

        // foreign keys
        public Guid? SphereId { get; set; }
        public string? SphereName { get; set; }

        public Guid? TypeId { get; set; }
        public string? TypeName { get; set; }

        public bool? Status { get; set; }
        public DateTime? Created { get; set; }
        public string? Comment { get; set; }
    }
}