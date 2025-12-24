namespace Backend.Models
{
    public class LoginRequest
    {
        public string Username { get; set; } = string.Empty;
        public string Password { get; set; } = string.Empty;
    }
    
    public class LoginResponse
    {
        public bool Success { get; set; }
        public string? Message { get; set; }
        public string? Token { get; set; }
        public User? User { get; set; }
    }
    
    public class SubmitDataRequest
    {
        public string Name { get; set; } = string.Empty;
        public string Email { get; set; } = string.Empty;
    }
    
    public class SubmitDataResponse
    {
        public bool Success { get; set; }
        public string? Message { get; set; }
    }
}