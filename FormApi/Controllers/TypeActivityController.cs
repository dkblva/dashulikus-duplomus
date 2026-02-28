using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using FormApi.Data;
using FormApi.Models;
using FormApi.Dtos.TypeActivity;

namespace FormApi.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class TypeActivityController : ControllerBase
    {
        private readonly ApplicationContext _context;

        public TypeActivityController(ApplicationContext context)
        {
            _context = context;
        }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<ReadTypeActivityDto>>> GetAll()
        {
            var list = await _context.TypeActivities
                .Select(t => new ReadTypeActivityDto { Id = t.Id, NameType = t.NameType })
                .ToListAsync();
            return list;
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<ReadTypeActivityDto>> GetById(Guid id)
        {
            var t = await _context.TypeActivities.FindAsync(id);
            if (t == null) return NotFound();
            return new ReadTypeActivityDto { Id = t.Id, NameType = t.NameType };
        }

        [HttpPost]
        public async Task<ActionResult<ReadTypeActivityDto>> Create(CreateTypeActivityDto dto)
        {
            var type = new TypeActivity { Id = Guid.NewGuid(), NameType = dto.NameType };
            _context.TypeActivities.Add(type);
            await _context.SaveChangesAsync();
            return CreatedAtAction(nameof(GetById), new { id = type.Id }, new ReadTypeActivityDto { Id = type.Id, NameType = type.NameType });
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> Update(Guid id, UpdateTypeActivityDto dto)
        {
            var type = await _context.TypeActivities.FindAsync(id);
            if (type == null) return NotFound();
            type.NameType = dto.NameType;
            await _context.SaveChangesAsync();
            return NoContent();
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> Delete(Guid id)
        {
            var item = await _context.TypeActivities.FindAsync(id);
            if (item == null)
                return NotFound();

            _context.TypeActivities.Remove(item);
            await _context.SaveChangesAsync();

            return NoContent();
        }
    }
}