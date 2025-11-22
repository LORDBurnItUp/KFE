# KFE - Hostinger API MCP Server

A Model Context Protocol (MCP) server for integrating Hostinger API with Claude Code. This server enables Claude to interact with your Hostinger hosting account, manage domains, DNS records, email accounts, and more.

## Features

The Hostinger API MCP server provides the following capabilities:

- **Domain Management**
  - List all domains in your account
  - Get detailed domain information

- **DNS Management**
  - List DNS records for a domain
  - Create new DNS records (A, AAAA, CNAME, MX, TXT, NS, SRV, CAA)
  - Update existing DNS records
  - Delete DNS records

- **Email Management**
  - List email accounts for a domain
  - Create new email accounts

- **Hosting Information**
  - Get hosting plan details
  - Get website statistics

## Setup

### Prerequisites

- Node.js 18.0.0 or higher
- A Hostinger account with API access
- Claude Code installed

### Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Get your Hostinger API token:**
   - Log in to your Hostinger account
   - Go to https://hpanel.hostinger.com/api-tokens
   - Create a new API token
   - Copy the token (you'll only see it once!)

3. **Configure your API token:**

   Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your API token:
   ```
   HOSTINGER_API_TOKEN=your_actual_api_token_here
   ```

4. **Load the environment variable:**

   Before using Claude Code, make sure to export the token:
   ```bash
   export $(cat .env | xargs)
   ```

   Or add it to your shell profile (~/.bashrc, ~/.zshrc, etc.):
   ```bash
   echo 'export HOSTINGER_API_TOKEN="your_token_here"' >> ~/.bashrc
   source ~/.bashrc
   ```

### Configuration

The MCP server is configured in `.claude/mcp.json`. This file tells Claude Code how to launch and communicate with the Hostinger API server.

The configuration is already set up and ready to use. Claude Code will automatically load this configuration when it starts.

## Usage

Once configured, you can use Claude Code to interact with your Hostinger account. Here are some example commands you can ask Claude:

### Domain Operations
- "List all my domains"
- "Get information about example.com"
- "Show me the DNS records for example.com"

### DNS Management
- "Add an A record for subdomain.example.com pointing to 192.0.2.1"
- "Create a CNAME record for www pointing to example.com"
- "Update the DNS record with ID abc123 to point to 192.0.2.2"
- "Delete the DNS record with ID abc123"

### Email Management
- "List all email accounts for example.com"
- "Create an email account info@example.com"

### Hosting Info
- "Show me my hosting plan details"
- "Get website statistics for example.com"

## Available MCP Tools

The following tools are available through the MCP server:

1. `list_domains` - List all domains
2. `get_domain_info` - Get domain details
3. `list_dns_records` - List DNS records
4. `create_dns_record` - Create a DNS record
5. `update_dns_record` - Update a DNS record
6. `delete_dns_record` - Delete a DNS record
7. `list_email_accounts` - List email accounts
8. `create_email_account` - Create an email account
9. `get_hosting_info` - Get hosting information
10. `get_website_stats` - Get website statistics

## Project Structure

```
KFE/
├── .claude/
│   └── mcp.json              # MCP server configuration
├── mcp-server/
│   └── hostinger-server.js   # Hostinger API MCP server implementation
├── .env.example              # Environment variable template
├── .gitignore                # Git ignore rules
├── package.json              # Node.js dependencies
└── README.md                 # This file
```

## Security Notes

- Never commit your `.env` file or expose your API token
- The `.gitignore` file is configured to exclude `.env` from version control
- Your API token has full access to your Hostinger account - keep it secure
- Consider using environment-specific tokens if available

## Troubleshooting

### "HOSTINGER_API_TOKEN environment variable is required"
Make sure you've created the `.env` file and exported the variable:
```bash
export $(cat .env | xargs)
```

### "Module not found" errors
Install the dependencies:
```bash
npm install
```

### "API error: 401"
Your API token is invalid or expired. Generate a new token from the Hostinger panel.

### MCP server not connecting
1. Check that Node.js 18+ is installed: `node --version`
2. Verify the `.claude/mcp.json` configuration is correct
3. Ensure the environment variable is set: `echo $HOSTINGER_API_TOKEN`

## API Documentation

For more information about the Hostinger API, visit:
- Hostinger API Documentation: https://hostinger.com/api-documentation
- API Token Management: https://hpanel.hostinger.com/api-tokens

## License

MIT