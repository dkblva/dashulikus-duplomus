using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using FormApi.Data;
using FormApi.Models;

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
        public async Task<ActionResult<IEnumerable<SphereActivity>>> GetAll()
        {
            return await _context.SphereActivities.ToListAsync();
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<SphereActivity>> GetById(Guid id)
        {
            var item = await _context.SphereActivities.FindAsync(id);

            if (item == null)
                return NotFound();

            return item;
        }

        [HttpPost]
        public async Task<ActionResult<SphereActivity>> Create(SphereActivity item)
        {
            item.Id = Guid.NewGuid();

            _context.SphereActivities.Add(item);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetById), new { id = item.Id }, item);
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> Update(Guid id, SphereActivity item)
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
            var item = await _context.SphereActivities.FindAsync(id);
            if (item == null)
                return NotFound();

            _context.SphereActivities.Remove(item);
            await _context.SaveChangesAsync();

            return NoContent();
        }
    }
}