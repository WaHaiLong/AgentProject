using Backend.Models;
using Microsoft.EntityFrameworkCore;
using System.Security.Cryptography;
using System.Text;

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

            // Verify password hash
            if (!VerifyPassword(request.Password, user.PasswordHash))
            {
                return new LoginResponse
                {
                    Success = false,
                    Message = "密码错误"
                };
            }

            return new LoginResponse
            {
                Success = true,
                Message = "登录成功",
                User = user
            };
        }

        public async Task<RegisterResponse> RegisterAsync(RegisterRequest request)
        {
            // Validate input
            if (string.IsNullOrWhiteSpace(request.Username) || 
                string.IsNullOrWhiteSpace(request.Email) || 
                string.IsNullOrWhiteSpace(request.Password))
            {
                return new RegisterResponse
                {
                    Success = false,
                    Message = "所有字段都必须填写"
                };
            }

            // Validate password confirmation
            if (request.Password != request.ConfirmPassword)
            {
                return new RegisterResponse
                {
                    Success = false,
                    Message = "两次输入的密码不一致"
                };
            }

            // Check password strength
            if (request.Password.Length < 6)
            {
                return new RegisterResponse
                {
                    Success = false,
                    Message = "密码长度至少为6位"
                };
            }

            // Check if username already exists
            var existingUser = await _context.Users
                .FirstOrDefaultAsync(u => u.Username == request.Username);
            
            if (existingUser != null)
            {
                return new RegisterResponse
                {
                    Success = false,
                    Message = "用户名已存在"
                };
            }

            // Check if email already exists
            var existingEmail = await _context.Users
                .FirstOrDefaultAsync(u => u.Email == request.Email);
            
            if (existingEmail != null)
            {
                return new RegisterResponse
                {
                    Success = false,
                    Message = "邮箱已被注册"
                };
            }

            // Create new user
            var user = new User
            {
                Username = request.Username,
                Email = request.Email,
                PasswordHash = HashPassword(request.Password),
                CreatedAt = DateTime.UtcNow
            };

            _context.Users.Add(user);
            await _context.SaveChangesAsync();

            return new RegisterResponse
            {
                Success = true,
                Message = "注册成功",
                User = user
            };
        }

        public async Task<bool> ValidateUserAsync(string username, string password)
        {
            var user = await _context.Users
                .FirstOrDefaultAsync(u => u.Username == username);

            if (user == null)
            {
                return false;
            }

            return VerifyPassword(password, user.PasswordHash);
        }

        private string HashPassword(string password)
        {
            using (var sha256 = SHA256.Create())
            {
                var bytes = Encoding.UTF8.GetBytes(password);
                var hash = sha256.ComputeHash(bytes);
                return Convert.ToBase64String(hash);
            }
        }

        private bool VerifyPassword(string password, string passwordHash)
        {
            var hash = HashPassword(password);
            return hash == passwordHash;
        }
    }
}