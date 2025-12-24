using Microsoft.EntityFrameworkCore;

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
                    PasswordHash = "test_pass123_hash" // In real app, this would be a proper hash
                },
                new User 
                { 
                    Username = "admin", 
                    Email = "admin@example.com", 
                    PasswordHash = "admin_pass123_hash" 
                }
            };

            foreach (User u in users)
            {
                context.Users.Add(u);
            }
            
            context.SaveChanges();
        }
    }
}