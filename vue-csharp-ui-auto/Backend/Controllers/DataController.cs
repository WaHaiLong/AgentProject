using Backend.Models;
using Backend.Services;
using Microsoft.AspNetCore.Mvc;

namespace Backend.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class DataController : ControllerBase
    {
        private readonly IDataService _dataService;

        public DataController(IDataService dataService)
        {
            _dataService = dataService;
        }

        [HttpPost("submit")]
        public async Task<ActionResult<SubmitDataResponse>> Submit([FromBody] SubmitDataRequest request)
        {
            var response = await _dataService.SubmitDataAsync(request);
            return Ok(response);
        }
    }
}