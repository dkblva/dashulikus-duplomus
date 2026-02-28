using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using FormApi.Data;
using FormApi.Models;
using FormApi.Dtos.Solution;

namespace FormApi.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class SolutionController : ControllerBase
    {
        private readonly ApplicationContext _context;

        public SolutionController(ApplicationContext context)
        {
            _context = context;
        }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<ReadSolutionDto>>> GetAll()
        {
            var list = await _context.Solutions
                .Select(s => new ReadSolutionDto
                {
                    Id = s.Id,
                    Description = s.Description,
                    IdApplication = s.IdApplication,
                    IdTarif = s.IdTarif
                })
                .ToListAsync();
            return list;
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<ReadSolutionDto>> GetById(Guid id)
        {
            var s = await _context.Solutions.FindAsync(id);

            if (s == null)
                return NotFound();

            return new ReadSolutionDto
            {
                Id = s.Id,
                Description = s.Description,
                IdApplication = s.IdApplication,
                IdTarif = s.IdTarif
            };
        }

        [HttpPost]
        public async Task<ActionResult<ReadSolutionDto>> Create(CreateSolutionDto dto)
        {
            // validate foreign keys
            var appExists = await _context.Applications.AnyAsync(a => a.Id == dto.IdApplication);
            if (!appExists)
                return BadRequest("Referenced application does not exist.");
            var tarifExists = await _context.Tarifs.AnyAsync(t => t.Id == dto.IdTarif);
            if (!tarifExists)
                return BadRequest("Referenced tarif does not exist.");

            var solution = new Solution
            {
                Id = Guid.NewGuid(),
                Description = dto.Description,
                IdApplication = dto.IdApplication,
                IdTarif = dto.IdTarif
            };

            _context.Solutions.Add(solution);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetById), new { id = solution.Id }, new ReadSolutionDto
            {
                Id = solution.Id,
                Description = solution.Description,
                IdApplication = solution.IdApplication,
                IdTarif = solution.IdTarif
            });
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> Update(Guid id, UpdateSolutionDto dto)
        {
            var solution = await _context.Solutions.FindAsync(id);
            if (solution == null)
                return NotFound();

            // validate related ids
            var appExists = await _context.Applications.AnyAsync(a => a.Id == dto.IdApplication);
            if (!appExists)
                return BadRequest("Referenced application does not exist.");
            var tarifExists = await _context.Tarifs.AnyAsync(t => t.Id == dto.IdTarif);
            if (!tarifExists)
                return BadRequest("Referenced tarif does not exist.");

            solution.Description = dto.Description;
            solution.IdApplication = dto.IdApplication;
            solution.IdTarif = dto.IdTarif;

            await _context.SaveChangesAsync();

            return NoContent();
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> Delete(Guid id)
        {
            var solution = await _context.Solutions.FindAsync(id);
            if (solution == null)
                return NotFound();

            _context.Solutions.Remove(solution);
            await _context.SaveChangesAsync();

            return NoContent();
        }
    }
}