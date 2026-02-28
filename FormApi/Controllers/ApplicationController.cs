using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using FormApi.Data;
using FormApi.Models;

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
        public async Task<ActionResult<IEnumerable<Application>>> GetAll()
        {
            return await _context.Applications
                .Include(a => a.SphereId)
                .Include(a => a.TypeId)
                .ToListAsync();
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<Application>> GetById(Guid id)
        {
            var application = await _context.Applications
                .Include(a => a.SphereActivity)
                .Include(a => a.TypeActivity)
                .FirstOrDefaultAsync(a => a.Id == id);

            if (application == null)
                return NotFound();

            return application;
        }

        [HttpPost("create")]
        public async Task<ActionResult<Application>> Create(Application application)
        {
            application.Id = Guid.NewGuid();

            //var app = new Application({
            //    Id = application.Id,
            //    FullName = 
            //});

            _context.Applications.Add(application);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetById), new { id = application.Id }, application);
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> Update(Guid id, Application application)
        {
            if (id != application.Id)
                return BadRequest();

            _context.Entry(application).State = EntityState.Modified;
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