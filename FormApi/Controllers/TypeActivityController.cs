using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using FormApi.Data;
using FormApi.Models;

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
        public async Task<ActionResult<IEnumerable<TypeActivity>>> GetAll()
        {
            return await _context.TypeActivities.ToListAsync();
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<TypeActivity>> GetById(Guid id)
        {
            var item = await _context.TypeActivities.FindAsync(id);

            if (item == null)
                return NotFound();

            return item;
        }

        [HttpPost]
        public async Task<ActionResult<TypeActivity>> Create(TypeActivity item)
        {
            item.Id = Guid.NewGuid();

            _context.TypeActivities.Add(item);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetById), new { id = item.Id }, item);
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> Update(Guid id, TypeActivity item)
        {
            if (id != item.Id)
                return BadRequest();

            _context.Entry(item).State = EntityState.Modified;
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