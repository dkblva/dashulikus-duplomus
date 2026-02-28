using FormApi.Data;
using FormApi.Dtos.Application;
using FormApi.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace FormApi.Controllers
{
    [ApiController]
    [Route("api/applications")]
    public class ApplicationController : ControllerBase
    {
        private readonly ApplicationContext _context;

        public ApplicationController(ApplicationContext context)
        {
            _context = context;
        }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<ReadApplicationDto>>> GetAll()
        {
            // project into DTOs including related names
            var list = await _context.Applications
                .Include(a => a.SphereActivity)
                .Include(a => a.TypeActivity)
                .Select(a => new ReadApplicationDto
                {
                    Id = a.Id,
                    FullName = a.FullName,
                    PhoneNumber = a.PhoneNumber,
                    Email = a.Email,
                    OrganizationName = a.OrganizationName,
                    SphereId = a.SphereId,
                    SphereName = a.SphereActivity != null ? a.SphereActivity.NameSphere : null,
                    TypeId = a.TypeId,
                    TypeName = a.TypeActivity != null ? a.TypeActivity.NameType : null,
                    Status = a.Status,
                    Created = a.Created,
                    Comment = a.Comment
                })
                .ToListAsync();

            return list;
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<ReadApplicationDto>> GetById(Guid id)
        {
            var a = await _context.Applications
                .Include(a => a.SphereActivity)
                .Include(a => a.TypeActivity)
                .FirstOrDefaultAsync(a => a.Id == id);

            if (a == null)
                return NotFound();

            var dto = new ReadApplicationDto
            {
                Id = a.Id,
                FullName = a.FullName,
                PhoneNumber = a.PhoneNumber,
                Email = a.Email,
                OrganizationName = a.OrganizationName,
                SphereId = a.SphereId,
                SphereName = a.SphereActivity?.NameSphere,
                TypeId = a.TypeId,
                TypeName = a.TypeActivity?.NameType,
                Status = a.Status,
                Created = a.Created,
                Comment = a.Comment
            };

            return dto;
        }

        [HttpPost]
        public async Task<ActionResult<ReadApplicationDto>> Create(CreateApplicationDto dto)
        {
            // verify that related ids exist if provided
            if (dto.SphereId != Guid.Empty)
            {
                var sphereExists = await _context.SphereActivities.AnyAsync(s => s.Id == dto.SphereId);
                if (!sphereExists)
                    return BadRequest("SphereActivity with given id does not exist.");
            }
            if (dto.TypeId != Guid.Empty)
            {
                var typeExists = await _context.TypeActivities.AnyAsync(t => t.Id == dto.TypeId);
                if (!typeExists)
                    return BadRequest("TypeActivity with given id does not exist.");
            }

            var application = new Application
            {
                Id = Guid.NewGuid(),
                FullName = dto.FullName,
                PhoneNumber = dto.PhoneNumber,
                Email = dto.Email,
                OrganizationName = dto.OrganizationName,
                SphereId = dto.SphereId == Guid.Empty ? null : dto.SphereId,
                TypeId = dto.TypeId == Guid.Empty ? null : dto.TypeId,
                Status = dto.Status,
                Created = dto.Created,
                Comment = dto.Comment
            };

            _context.Applications.Add(application);
            await _context.SaveChangesAsync();

            // return created resource as read dto
            var resultDto = new ReadApplicationDto
            {
                Id = application.Id,
                FullName = application.FullName,
                PhoneNumber = application.PhoneNumber,
                Email = application.Email,
                OrganizationName = application.OrganizationName,
                SphereId = application.SphereId,
                SphereName = (await _context.SphereActivities.FindAsync(application.SphereId))?.NameSphere,
                TypeId = application.TypeId,
                TypeName = (await _context.TypeActivities.FindAsync(application.TypeId))?.NameType,
                Status = application.Status,
                Created = application.Created,
                Comment = application.Comment
            };

            return CreatedAtAction(nameof(GetById), new { id = application.Id }, resultDto);
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> Update(Guid id, UpdateApplicationDto dto)
        {
            var application = await _context.Applications.FindAsync(id);
            if (application == null)
                return NotFound();

            // validate foreign keys
            if (dto.SphereId != null && dto.SphereId != Guid.Empty)
            {
                var sphereExists = await _context.SphereActivities.AnyAsync(s => s.Id == dto.SphereId);
                if (!sphereExists)
                    return BadRequest("SphereActivity with given id does not exist.");
            }
            if (dto.TypeId != null && dto.TypeId != Guid.Empty)
            {
                var typeExists = await _context.TypeActivities.AnyAsync(t => t.Id == dto.TypeId);
                if (!typeExists)
                    return BadRequest("TypeActivity with given id does not exist.");
            }

            application.FullName = dto.FullName;
            application.PhoneNumber = dto.PhoneNumber;
            application.Email = dto.Email;
            application.OrganizationName = dto.OrganizationName;
            application.SphereId = dto.SphereId;
            application.TypeId = dto.TypeId;
            application.Status = dto.Status;
            application.Created = dto.Created ?? application.Created;
            application.Comment = dto.Comment;

            await _context.SaveChangesAsync();

            return NoContent();
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> Delete(Guid id)
        {
            var application = await _context.Applications.FindAsync(id);
            if (application == null)
                return NotFound();

            _context.Applications.Remove(application);
            await _context.SaveChangesAsync();

            return NoContent();
        }
    }
}