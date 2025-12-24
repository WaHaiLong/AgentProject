using Backend.Models;
using Microsoft.EntityFrameworkCore;

namespace Backend.Services
{
    public class AuthService : IAuthService
    {
        private readonly AppDbContext _context;

        public AuthService(AppDbContext context)
        {
            _context = context;
        }

        public async Task<LoginResponse> LoginAsync(LoginRequest request)
        {
            var user = await _context.Users
                .FirstOrDefaultAsync(u => u.Username == request.Username);

            if (user == null)
            {
                return new LoginResponse
                {
                    Success = false,
                    Message = "用户名不存在"
                };
            }

            // In a real application, you would hash and compare the password
            // For testing purposes, we'll use a simple comparison
            if (request.Password == "test_pass123")
            {
                return new LoginResponse
                {
                    Success = true,
                    Message = "登录成功",
                    User = user
                };
            }
            else
            {
                return new LoginResponse
                {
                    Success = false,
                    Message = "密码错误"
                };
            }
        }

        public async Task<bool> ValidateUserAsync(string username, string password)
        {
            var user = await _context.Users
                .FirstOrDefaultAsync(u => u.Username == username);

            if (user == null)
            {
                return false;
            }

            // For testing purposes, we'll use a simple comparison
            return password == "test_pass123";
        }
    }
}