using Backend.Models;

namespace Backend.Services
{
    public interface IDataService
    {
        Task<SubmitDataResponse> SubmitDataAsync(SubmitDataRequest request);
    }
}