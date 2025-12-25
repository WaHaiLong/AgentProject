using Backend.Models;

namespace Backend.Services
{
    public class DataService : IDataService
    {
        public Task<SubmitDataResponse> SubmitDataAsync(SubmitDataRequest request)
        {
            // Simulate processing the submitted data
            // In a real application, this would save to database or perform business logic
            
            // Validate input
            if (string.IsNullOrWhiteSpace(request.Name) || string.IsNullOrWhiteSpace(request.Email))
            {
                return Task.FromResult(new SubmitDataResponse
                {
                    Success = false,
                    Message = "姓名和邮箱不能为空"
                });
            }

            // Simulate successful processing
            return Task.FromResult(new SubmitDataResponse
            {
                Success = true,
                Message = $"数据已成功提交: {request.Name} ({request.Email})"
            });
        }
    }
}