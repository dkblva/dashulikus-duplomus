using System;
using System.ComponentModel.DataAnnotations;

namespace FormApi.Dtos.Application
{
    public class UpdateApplicationDto
    {
        [Required]
        public string FullName { get; set; } = null!;

        public string? PhoneNumber { get; set; }
        public string? Email { get; set; }
        public string? OrganizationName { get; set; }

        // foreign keys -- allow null to disassociate
        public Guid? SphereId { get; set; }
        public Guid? TypeId { get; set; }

        public bool? Status { get; set; }
        // created date should normally not be changed but allow if necessary
        public DateTime? Created { get; set; }
        public string? Comment { get; set; }
    }
}