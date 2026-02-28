using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using FormApi.Data;
using FormApi.Models;
using FormApi.Dtos.Tarif;

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
        public async Task<ActionResult<IEnumerable<ReadTarifDto>>> GetAll()
        {
            var list = await _context.Tarifs
                .Select(t => new ReadTarifDto { Id = t.Id, Name = t.Name, Description = t.Description, Price = t.Price })
                .ToListAsync();
            return list;
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<ReadTarifDto>> GetById(Guid id)
        {
            var t = await _context.Tarifs.FindAsync(id);
            if (t == null) return NotFound();
            return new ReadTarifDto { Id = t.Id, Name = t.Name, Description = t.Description, Price = t.Price };
        }

        [HttpPost]
        public async Task<ActionResult<ReadTarifDto>> Create(CreateTarifDto dto)
        {
            if (!ModelState.IsValid)
                return ValidationProblem(ModelState);
            var tarif = new Tarif { Id = Guid.NewGuid(), Name = dto.Name, Description = dto.Description, Price = dto.Price };
            _context.Tarifs.Add(tarif);
            await _context.SaveChangesAsync();
            return CreatedAtAction(nameof(GetById), new { id = tarif.Id }, new ReadTarifDto { Id = tarif.Id, Name = tarif.Name, Description = tarif.Description, Price = tarif.Price });
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> Update(Guid id, UpdateTarifDto dto)
        {
            if (!ModelState.IsValid)
                return ValidationProblem(ModelState);
            var tarif = await _context.Tarifs.FindAsync(id);
            if (tarif == null) return NotFound();
            tarif.Name = dto.Name;
            tarif.Description = dto.Description;
            tarif.Price = dto.Price;
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