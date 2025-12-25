using Microsoft.EntityFrameworkCore;
using System.Security.Cryptography;
using System.Text;

namespace Backend.Models
{
    public static class DbInitializer
    {
        public static void Initialize(AppDbContext context)
        {
            context.Database.EnsureCreated();

            if (context.Users.Any())
            {
                return; // DB has been seeded
            }

            var users = new User[]
            {
                new User 
                { 
                    Username = "test_user", 
                    Email = "test@example.com", 
                    PasswordHash = HashPassword("test123") // 密码: test123
                },
                new User 
                { 
                    Username = "admin", 
                    Email = "admin@example.com", 
                    PasswordHash = HashPassword("admin123") // 密码: admin123
                }
            };

            foreach (User u in users)
            {
                context.Users.Add(u);
            }
            
            context.SaveChanges();
        }

        private static string HashPassword(string password)
        {
            using (var sha256 = SHA256.Create())
            {
                var bytes = Encoding.UTF8.GetBytes(password);
                var hash = sha256.ComputeHash(bytes);
                return Convert.ToBase64String(hash);
            }
        }
    }
}