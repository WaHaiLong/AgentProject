using Backend.Models;

namespace Backend.Services
{
    public interface IAuthService
    {
        Task<LoginResponse> LoginAsync(LoginRequest request);
        Task<bool> ValidateUserAsync(string username, string password);
    }
}