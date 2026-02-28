using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using FormApi.Data;
using FormApi.Models;

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
        public async Task<ActionResult<IEnumerable<Solution>>> GetAll()
        {
            return await _context.Solutions.ToListAsync();
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<Solution>> GetById(Guid id)
        {
            var solution = await _context.Solutions.FindAsync(id);

            if (solution == null)
                return NotFound();

            return solution;
        }

        [HttpPost]
        public async Task<ActionResult<Solution>> Create(Solution solution)
        {
            solution.Id = Guid.NewGuid(); // если Id не генерируется автоматически

            _context.Solutions.Add(solution);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetById), new { id = solution.Id }, solution);
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> Update(Guid id, Solution solution)
        {
            if (id != solution.Id)
                return BadRequest();

            _context.Entry(solution).State = EntityState.Modified;
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