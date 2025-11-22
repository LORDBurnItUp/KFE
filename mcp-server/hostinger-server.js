#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

const API_TOKEN = process.env.HOSTINGER_API_TOKEN;
const API_BASE_URL = 'https://api.hostinger.com/v1';

if (!API_TOKEN) {
  console.error('HOSTINGER_API_TOKEN environment variable is required');
  process.exit(1);
}

// Helper function to make API requests
async function makeHostingerRequest(endpoint, method = 'GET', body = null) {
  const url = `${API_BASE_URL}${endpoint}`;
  const options = {
    method,
    headers: {
      'Authorization': `Bearer ${API_TOKEN}`,
      'Content-Type': 'application/json',
    },
  };

  if (body && method !== 'GET') {
    options.body = JSON.stringify(body);
  }

  try {
    const response = await fetch(url, options);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(`Hostinger API error: ${response.status} - ${JSON.stringify(data)}`);
    }

    return data;
  } catch (error) {
    throw new Error(`Failed to make Hostinger API request: ${error.message}`);
  }
}

// Create server instance
const server = new Server(
  {
    name: 'hostinger-api-server',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'list_domains',
        description: 'List all domains in your Hostinger account',
        inputSchema: {
          type: 'object',
          properties: {},
        },
      },
      {
        name: 'get_domain_info',
        description: 'Get detailed information about a specific domain',
        inputSchema: {
          type: 'object',
          properties: {
            domain: {
              type: 'string',
              description: 'The domain name to get information about',
            },
          },
          required: ['domain'],
        },
      },
      {
        name: 'list_dns_records',
        description: 'List DNS records for a specific domain',
        inputSchema: {
          type: 'object',
          properties: {
            domain: {
              type: 'string',
              description: 'The domain name to list DNS records for',
            },
          },
          required: ['domain'],
        },
      },
      {
        name: 'create_dns_record',
        description: 'Create a new DNS record for a domain',
        inputSchema: {
          type: 'object',
          properties: {
            domain: {
              type: 'string',
              description: 'The domain name',
            },
            type: {
              type: 'string',
              description: 'DNS record type (A, AAAA, CNAME, MX, TXT, etc.)',
              enum: ['A', 'AAAA', 'CNAME', 'MX', 'TXT', 'NS', 'SRV', 'CAA'],
            },
            name: {
              type: 'string',
              description: 'Record name/subdomain (use @ for root domain)',
            },
            content: {
              type: 'string',
              description: 'Record content/value',
            },
            ttl: {
              type: 'number',
              description: 'Time to live in seconds (optional, default: 3600)',
            },
            priority: {
              type: 'number',
              description: 'Priority for MX records (optional)',
            },
          },
          required: ['domain', 'type', 'name', 'content'],
        },
      },
      {
        name: 'update_dns_record',
        description: 'Update an existing DNS record',
        inputSchema: {
          type: 'object',
          properties: {
            domain: {
              type: 'string',
              description: 'The domain name',
            },
            record_id: {
              type: 'string',
              description: 'The DNS record ID to update',
            },
            content: {
              type: 'string',
              description: 'New record content/value',
            },
            ttl: {
              type: 'number',
              description: 'Time to live in seconds (optional)',
            },
          },
          required: ['domain', 'record_id', 'content'],
        },
      },
      {
        name: 'delete_dns_record',
        description: 'Delete a DNS record',
        inputSchema: {
          type: 'object',
          properties: {
            domain: {
              type: 'string',
              description: 'The domain name',
            },
            record_id: {
              type: 'string',
              description: 'The DNS record ID to delete',
            },
          },
          required: ['domain', 'record_id'],
        },
      },
      {
        name: 'list_email_accounts',
        description: 'List email accounts for a specific domain',
        inputSchema: {
          type: 'object',
          properties: {
            domain: {
              type: 'string',
              description: 'The domain name to list email accounts for',
            },
          },
          required: ['domain'],
        },
      },
      {
        name: 'create_email_account',
        description: 'Create a new email account',
        inputSchema: {
          type: 'object',
          properties: {
            domain: {
              type: 'string',
              description: 'The domain name',
            },
            email: {
              type: 'string',
              description: 'Email address to create (e.g., user@domain.com)',
            },
            password: {
              type: 'string',
              description: 'Password for the email account',
            },
          },
          required: ['domain', 'email', 'password'],
        },
      },
      {
        name: 'get_hosting_info',
        description: 'Get information about your hosting plan',
        inputSchema: {
          type: 'object',
          properties: {},
        },
      },
      {
        name: 'get_website_stats',
        description: 'Get website statistics for a domain',
        inputSchema: {
          type: 'object',
          properties: {
            domain: {
              type: 'string',
              description: 'The domain name to get statistics for',
            },
          },
          required: ['domain'],
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case 'list_domains': {
        const data = await makeHostingerRequest('/domains');
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(data, null, 2),
            },
          ],
        };
      }

      case 'get_domain_info': {
        const { domain } = args;
        const data = await makeHostingerRequest(`/domains/${domain}`);
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(data, null, 2),
            },
          ],
        };
      }

      case 'list_dns_records': {
        const { domain } = args;
        const data = await makeHostingerRequest(`/domains/${domain}/dns`);
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(data, null, 2),
            },
          ],
        };
      }

      case 'create_dns_record': {
        const { domain, type, name, content, ttl, priority } = args;
        const body = {
          type,
          name,
          content,
          ...(ttl && { ttl }),
          ...(priority && { priority }),
        };
        const data = await makeHostingerRequest(`/domains/${domain}/dns`, 'POST', body);
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(data, null, 2),
            },
          ],
        };
      }

      case 'update_dns_record': {
        const { domain, record_id, content, ttl } = args;
        const body = {
          content,
          ...(ttl && { ttl }),
        };
        const data = await makeHostingerRequest(
          `/domains/${domain}/dns/${record_id}`,
          'PUT',
          body
        );
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(data, null, 2),
            },
          ],
        };
      }

      case 'delete_dns_record': {
        const { domain, record_id } = args;
        const data = await makeHostingerRequest(
          `/domains/${domain}/dns/${record_id}`,
          'DELETE'
        );
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(data, null, 2),
            },
          ],
        };
      }

      case 'list_email_accounts': {
        const { domain } = args;
        const data = await makeHostingerRequest(`/domains/${domain}/emails`);
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(data, null, 2),
            },
          ],
        };
      }

      case 'create_email_account': {
        const { domain, email, password } = args;
        const body = { email, password };
        const data = await makeHostingerRequest(`/domains/${domain}/emails`, 'POST', body);
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(data, null, 2),
            },
          ],
        };
      }

      case 'get_hosting_info': {
        const data = await makeHostingerRequest('/hosting');
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(data, null, 2),
            },
          ],
        };
      }

      case 'get_website_stats': {
        const { domain } = args;
        const data = await makeHostingerRequest(`/domains/${domain}/stats`);
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(data, null, 2),
            },
          ],
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    return {
      content: [
        {
          type: 'text',
          text: `Error: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
});

// Start the server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Hostinger API MCP Server running on stdio');
}

main().catch((error) => {
  console.error('Fatal error in main():', error);
  process.exit(1);
});
