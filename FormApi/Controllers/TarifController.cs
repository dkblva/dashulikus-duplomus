using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using FormApi.Data;
using FormApi.Models;

namespace FormApi.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class TarifController : ControllerBase
    {
        private readonly ApplicationContext _context;

        public TarifController(ApplicationContext context)
        {
            _context = context;
        }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<Tarif>>> GetAll()
        {
            return await _context.Tarifs.ToListAsync();
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<Tarif>> GetById(Guid id)
        {
            var tarif = await _context.Tarifs.FindAsync(id);

            if (tarif == null)
                return NotFound();

            return tarif;
        }

        [HttpPost]
        public async Task<ActionResult<Tarif>> Create(Tarif tarif)
        {
            tarif.Id = Guid.NewGuid();

            _context.Tarifs.Add(tarif);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetById), new { id = tarif.Id }, tarif);
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> Update(Guid id, Tarif tarif)
        {
            if (id != tarif.Id)
                return BadRequest();

            _context.Entry(tarif).State = EntityState.Modified;
            await _context.SaveChangesAsync();

            return NoContent();
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> Delete(Guid id)
        {
            var tarif = await _context.Tarifs.FindAsync(id);
            if (tarif == null)
                return NotFound();

            _context.Tarifs.Remove(tarif);
            await _context.SaveChangesAsync();

            return NoContent();
        }
    }
}