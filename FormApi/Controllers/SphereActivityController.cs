using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using FormApi.Data;
using FormApi.Models;
using FormApi.Dtos.SphereActivity;

namespace FormApi.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class SphereActivityController : ControllerBase
    {
        private readonly ApplicationContext _context;

        public SphereActivityController(ApplicationContext context)
        {
            _context = context;
        }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<ReadSphereActivityDto>>> GetAll()
        {
            var list = await _context.SphereActivities
                .Select(s => new ReadSphereActivityDto { Id = s.Id, NameSphere = s.NameSphere })
                .ToListAsync();
            return list;
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<ReadSphereActivityDto>> GetById(Guid id)
        {
            var s = await _context.SphereActivities.FindAsync(id);
            if (s == null)
                return NotFound();
            return new ReadSphereActivityDto { Id = s.Id, NameSphere = s.NameSphere };
        }

        [HttpPost]
        public async Task<ActionResult<ReadSphereActivityDto>> Create(CreateSphereActivityDto dto)
        {
            var sphere = new SphereActivity
            {
                Id = Guid.NewGuid(),
                NameSphere = dto.NameSphere
            };
            _context.SphereActivities.Add(sphere);
            await _context.SaveChangesAsync();
            return CreatedAtAction(nameof(GetById), new { id = sphere.Id }, new ReadSphereActivityDto { Id = sphere.Id, NameSphere = sphere.NameSphere });
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> Update(Guid id, UpdateSphereActivityDto dto)
        {
            var sphere = await _context.SphereActivities.FindAsync(id);
            if (sphere == null) return NotFound();
            sphere.NameSphere = dto.NameSphere;
            await _context.SaveChangesAsync();
            return NoContent();
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> Delete(Guid id)
        {
            var item = await _context.SphereActivities.FindAsync(id);
            if (item == null)
                return NotFound();

            _context.SphereActivities.Remove(item);
            await _context.SaveChangesAsync();

            return NoContent();
        }
    }
}