<ac:structured-macro ac:macro-id="3240cdd8-a656-400a-8a3c-37d6215f865d" ac:name="panel" ac:schema-version="1">
  <ac:parameter ac:name="borderColor">#ccc</ac:parameter>
  <ac:parameter ac:name="bgColor">#fff</ac:parameter>
  <ac:parameter ac:name="titleBGColor">#f4f5f7</ac:parameter>
  <ac:parameter ac:name="borderStyle">dashed</ac:parameter>
  <ac:parameter ac:name="title">&#55357;&#56523; Overview</ac:parameter>
  <ac:rich-text-body>
    <p>The <strong>JIRA, Bitbucket &amp; Confluence MCP Servers</strong> are Model Context Protocol (MCP) integrations that provide seamless access to JIRA, Bitbucket, and Confluence functionality directly from your IDE (VSCode). These tools enable developers and project managers to interact with JIRA tickets, projects, sprints, reports, Bitbucket repositories, pull requests, code reviews, and Confluence documentation without leaving their development environment.</p>
  </ac:rich-text-body>
</ac:structured-macro>
<hr/>
<h2>&#55356;&#57263; Key Benefits</h2>
<p>
  <span style="color:var(--ds-text-accent-blue,#0055cc);">
    <strong>&#55357;&#56960; Streamlined Workflow</strong>
  </span>: Access JIRA, Bitbucket, and Confluence directly from your IDE<br/>
  <span style="color:var(--ds-text-accent-blue,#0055cc);">
    <strong>⚡ Faster Development</strong>
  </span>: Reduce context switching between tools <br/>
  <span style="color:var(--ds-text-accent-blue,#0055cc);">
    <strong>&#55357;&#56522; Real-time Insights</strong>
  </span>: Get project status, sprint burndown, team metrics, PR status, and documentation instantly<br/>
  <span style="color:var(--ds-text-accent-blue,#0055cc);">
    <strong>&#55357;&#56580; Automated Setup</strong>
  </span>: One-click installation scripts for multiple platforms<br/>
  <span style="color:var(--ds-text-accent-blue,#0055cc);">
    <strong>&#55357;&#57057;️ Secure Authentication</strong>
  </span>: Token-based authentication with health checks<br/>
  <span style="color:var(--ds-text-accent-blue,#0055cc);">
    <strong>&#55357;&#56599; Integrated Development</strong>
  </span>: Link JIRA tickets with Bitbucket PRs and Confluence documentation seamlessly</p>
<hr/>
<h2>&#55357;&#57056;️ Available Tools &amp; Features</h2>
<ac:structured-macro ac:macro-id="5669df9f-554f-4535-a70c-1d0883032188" ac:name="deck" ac:schema-version="1">
  <ac:parameter ac:name="id">tools-tabs</ac:parameter>
  <ac:rich-text-body>
    <ac:structured-macro ac:macro-id="e9bc98fd-f782-4f41-b664-ad66b4123881" ac:name="card" ac:schema-version="1">
      <ac:parameter ac:name="label">&#55357;&#56615; JIRA Tools</ac:parameter>
      <ac:rich-text-body>
        <h3>Configuration &amp; Health Tools</h3>
        <table>
          <tbody>
            <tr>
              <th>
                <p>Tool</p>
              </th>
              <th>
                <p>Description</p>
              </th>
              <th>
                <p>Usage</p>
              </th>
            </tr>
            <tr>
              <td>
                <p>
                  <code>healthcheck</code>
                </p>
              </td>
              <td>
                <p>Verify JIRA configuration and auth token status</p>
              </td>
              <td>
                <p>Run after setup to ensure everything is working</p>
              </td>
            </tr>
            <tr>
              <td>
                <p>
                  <code>test_connection</code>
                </p>
              </td>
              <td>
                <p>Test JIRA connection and authentication</p>
              </td>
              <td>
                <p>Use after updating auth token to verify connectivity</p>
              </td>
            </tr>
          </tbody>
        </table>
        <ac:structured-macro ac:macro-id="b9a19f72-bd58-4709-9881-c6daee37c4b4" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">Ticket Management Tools</ac:parameter>
          <ac:rich-text-body>
            <table>
              <tbody>
                <tr>
                  <th>
                    <p>Tool</p>
                  </th>
                  <th>
                    <p>Description</p>
                  </th>
                  <th>
                    <p>Parameters</p>
                  </th>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>get_ticket_details</code>
                    </p>
                  </td>
                  <td>
                    <p>Get comprehensive details for a specific ticket</p>
                  </td>
                  <td>
                    <p>
                      <code>ticket_key</code> (e.g., "PROJ-123")</p>
                  </td>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>create_review_task</code>
                    </p>
                  </td>
                  <td>
                    <p>Create a code review task under a parent story</p>
                  </td>
                  <td>
                    <p>
                      <code>parent_key</code>, <code>title</code>, <code>description</code>
                    </p>
                  </td>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>create_user_story</code>
                    </p>
                  </td>
                  <td>
                    <p>Create a new user story with full Agile template</p>
                  </td>
                  <td>
                    <p>
                      <code>project_id</code>, <code>summary</code>, <code>description</code>, plus optional fields</p>
                  </td>
                </tr>
              </tbody>
            </table>
          </ac:rich-text-body>
        </ac:structured-macro>
        <ac:structured-macro ac:macro-id="6759dba4-1fb0-4b0d-8984-abd9660ebc46" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">Project &amp; Sprint Analytics</ac:parameter>
          <ac:rich-text-body>
            <table>
              <tbody>
                <tr>
                  <th>
                    <p>Tool</p>
                  </th>
                  <th>
                    <p>Description</p>
                  </th>
                  <th>
                    <p>Parameters</p>
                  </th>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>get_my_active_work</code>
                    </p>
                  </td>
                  <td>
                    <p>Get all active tickets assigned to current user</p>
                  </td>
                  <td>
                    <p>None</p>
                  </td>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>get_sprint_burndown</code>
                    </p>
                  </td>
                  <td>
                    <p>Get current sprint burndown data and progress</p>
                  </td>
                  <td>
                    <p>
                      <code>project_key</code> (default: "MS-TECH")</p>
                  </td>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>get_high_priority_blockers</code>
                    </p>
                  </td>
                  <td>
                    <p>Find high-priority tickets blocking progress</p>
                  </td>
                  <td>
                    <p>
                      <code>project_key</code> (default: "MS-TECH")</p>
                  </td>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>get_weekly_delivery_report</code>
                    </p>
                  </td>
                  <td>
                    <p>Weekly delivery metrics and completed work</p>
                  </td>
                  <td>
                    <p>
                      <code>project_key</code> (default: "MS-TECH")</p>
                  </td>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>get_bug_health_report</code>
                    </p>
                  </td>
                  <td>
                    <p>Bug statistics and health metrics</p>
                  </td>
                  <td>
                    <p>
                      <code>project_key</code> (default: "MS-TECH")</p>
                  </td>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>get_overdue_items</code>
                    </p>
                  </td>
                  <td>
                    <p>Find overdue tickets requiring attention</p>
                  </td>
                  <td>
                    <p>
                      <code>project_key</code> (default: "MS-TECH")</p>
                  </td>
                </tr>
              </tbody>
            </table>
          </ac:rich-text-body>
        </ac:structured-macro>
        <ac:structured-macro ac:macro-id="34b580c3-8cd2-4479-90c3-8c0a774616c7" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">Team Management</ac:parameter>
          <ac:rich-text-body>
            <table>
              <tbody>
                <tr>
                  <th>
                    <p>Tool</p>
                  </th>
                  <th>
                    <p>Description</p>
                  </th>
                  <th>
                    <p>Parameters</p>
                  </th>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>get_unassigned_work</code>
                    </p>
                  </td>
                  <td>
                    <p>Find unassigned tickets in project</p>
                  </td>
                  <td>
                    <p>
                      <code>project_key</code> (default: "MS-TECH")</p>
                  </td>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>get_team_workload</code>
                    </p>
                  </td>
                  <td>
                    <p>Get workload analysis for specific team member</p>
                  </td>
                  <td>
                    <p>
                      <code>assignee_name</code>
                    </p>
                  </td>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>get_recent_activity</code>
                    </p>
                  </td>
                  <td>
                    <p>Recent project activity and changes</p>
                  </td>
                  <td>
                    <p>
                      <code>project_key</code>, <code>days</code> (default: 3)</p>
                  </td>
                </tr>
              </tbody>
            </table>
          </ac:rich-text-body>
        </ac:structured-macro>
        <ac:structured-macro ac:macro-id="be09e3e0-b594-41ed-b49c-ba447b3754ad" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">Release Management</ac:parameter>
          <ac:rich-text-body>
            <table>
              <tbody>
                <tr>
                  <th>
                    <p>Tool</p>
                  </th>
                  <th>
                    <p>Description</p>
                  </th>
                  <th>
                    <p>Parameters</p>
                  </th>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>get_feature_progress</code>
                    </p>
                  </td>
                  <td>
                    <p>Track progress of features by label</p>
                  </td>
                  <td>
                    <p>
                      <code>feature_label</code>, <code>project_key</code> (optional)</p>
                  </td>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>get_release_readiness</code>
                    </p>
                  </td>
                  <td>
                    <p>Release readiness assessment</p>
                  </td>
                  <td>
                    <p>
                      <code>fix_version</code>, <code>project_key</code> (default: "MS-TECH")</p>
                  </td>
                </tr>
              </tbody>
            </table>
          </ac:rich-text-body>
        </ac:structured-macro>
        <ac:structured-macro ac:macro-id="dcdbb8f4-b11d-4d0f-9cc4-86284b046da8" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">Search &amp; Discovery</ac:parameter>
          <ac:rich-text-body>
            <table>
              <tbody>
                <tr>
                  <th>
                    <p>Tool</p>
                  </th>
                  <th>
                    <p>Description</p>
                  </th>
                  <th>
                    <p>Parameters</p>
                  </th>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>search_jira_custom</code>
                    </p>
                  </td>
                  <td>
                    <p>Execute custom JQL queries</p>
                  </td>
                  <td>
                    <p>
                      <code>jql_query</code>, <code>max_results</code> (default: 50)</p>
                  </td>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>get_user_projects</code>
                    </p>
                  </td>
                  <td>
                    <p>Get projects accessible to a user</p>
                  </td>
                  <td>
                    <p>
                      <code>username</code>
                    </p>
                  </td>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>get_projects</code>
                    </p>
                  </td>
                  <td>
                    <p>Search and list available projects</p>
                  </td>
                  <td>
                    <p>
                      <code>search_term</code>, <code>max_results</code>
                    </p>
                  </td>
                </tr>
              </tbody>
            </table>
          </ac:rich-text-body>
        </ac:structured-macro>
      </ac:rich-text-body>
    </ac:structured-macro>
    <ac:structured-macro ac:macro-id="58397456-cb75-49a1-b3a6-74a82ea2a20a" ac:name="card" ac:schema-version="1">
      <ac:parameter ac:name="label">&#55357;&#56615; Bitbucket Tools</ac:parameter>
      <ac:rich-text-body>
        <ac:structured-macro ac:macro-id="0ee1050a-9183-43ce-b962-d8af38f0aaeb" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">Pull Request Management</ac:parameter>
          <ac:rich-text-body>
            <table>
              <tbody>
                <tr>
                  <th>
                    <p>Tool</p>
                  </th>
                  <th>
                    <p>Description</p>
                  </th>
                  <th>
                    <p>Parameters</p>
                  </th>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>get_pr_details</code>
                    </p>
                  </td>
                  <td>
                    <p>Get comprehensive PR information and diffs</p>
                  </td>
                  <td>
                    <p>
                      <code>pr_link</code> (full PR URL)</p>
                  </td>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>add_pr_comment</code>
                    </p>
                  </td>
                  <td>
                    <p>Add comments to pull requests</p>
                  </td>
                  <td>
                    <p>
                      <code>pr_link</code>, <code>comment_text</code>, <code>line_comment</code> (optional)</p>
                  </td>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>get_reviewed_prs</code>
                    </p>
                  </td>
                  <td>
                    <p>Get PRs reviewed by a specific user</p>
                  </td>
                  <td>
                    <p>
                      <code>workspaces</code>, <code>repo_slugs</code>, <code>username</code>, <code>state</code>, <code>limit</code>
                    </p>
                  </td>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>get_pr_activities</code>
                    </p>
                  </td>
                  <td>
                    <p>Get PR activities and comment history</p>
                  </td>
                  <td>
                    <p>
                      <code>pr_link</code>
                    </p>
                  </td>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>create_pull_request</code>
                    </p>
                  </td>
                  <td>
                    <p>Create new pull requests</p>
                  </td>
                  <td>
                    <p>
                      <code>workspace</code>, <code>repo_slug</code>, <code>source_branch</code>, <code>target_branch</code>, <code>title</code>, etc.</p>
                  </td>
                </tr>
              </tbody>
            </table>
          </ac:rich-text-body>
        </ac:structured-macro>
        <ac:structured-macro ac:macro-id="74025cec-be32-4c24-b41d-f8730a3cae43" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">Repository Management</ac:parameter>
          <ac:rich-text-body>
            <table>
              <tbody>
                <tr>
                  <th>
                    <p>Tool</p>
                  </th>
                  <th>
                    <p>Description</p>
                  </th>
                  <th>
                    <p>Parameters</p>
                  </th>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>get_repository_info</code>
                    </p>
                  </td>
                  <td>
                    <p>Get detailed repository information</p>
                  </td>
                  <td>
                    <p>
                      <code>workspace</code>, <code>repo_slug</code>
                    </p>
                  </td>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>get_repository_branches</code>
                    </p>
                  </td>
                  <td>
                    <p>List and filter repository branches</p>
                  </td>
                  <td>
                    <p>
                      <code>workspace</code>, <code>repo_slug</code>, <code>filter_text</code> (optional)</p>
                  </td>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>get_file_content</code>
                    </p>
                  </td>
                  <td>
                    <p>Get content of specific files</p>
                  </td>
                  <td>
                    <p>
                      <code>workspace</code>, <code>repo_slug</code>, <code>file_path</code>, <code>ref</code> (optional)</p>
                  </td>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>get_repo_permissions</code>
                    </p>
                  </td>
                  <td>
                    <p>Get repository user permissions</p>
                  </td>
                  <td>
                    <p>
                      <code>workspace</code>, <code>repo_slug</code>
                    </p>
                  </td>
                </tr>
              </tbody>
            </table>
          </ac:rich-text-body>
        </ac:structured-macro>
        <ac:structured-macro ac:macro-id="cd83d698-073f-4947-b06a-c22732af9165" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">Code &amp; Commit Management</ac:parameter>
          <ac:rich-text-body>
            <table>
              <tbody>
                <tr>
                  <th>
                    <p>Tool</p>
                  </th>
                  <th>
                    <p>Description</p>
                  </th>
                  <th>
                    <p>Parameters</p>
                  </th>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>get_commit_details</code>
                    </p>
                  </td>
                  <td>
                    <p>Get detailed commit information</p>
                  </td>
                  <td>
                    <p>
                      <code>workspace</code>, <code>repo_slug</code>, <code>commit_id</code>
                    </p>
                  </td>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>bitbucket_healthcheck</code>
                    </p>
                  </td>
                  <td>
                    <p>Verify Bitbucket connectivity and setup</p>
                  </td>
                  <td>
                    <p>None</p>
                  </td>
                </tr>
              </tbody>
            </table>
          </ac:rich-text-body>
        </ac:structured-macro>
      </ac:rich-text-body>
    </ac:structured-macro>
    <ac:structured-macro ac:macro-id="48d2bc00-bf2a-4378-8e78-1292860ab583" ac:name="card" ac:schema-version="1">
      <ac:parameter ac:name="label">&#55357;&#56615; Confluence Tools</ac:parameter>
      <ac:rich-text-body>
        <h3>Configuration &amp; Health</h3>
        <table>
          <tbody>
            <tr>
              <th>
                <p>Tool</p>
              </th>
              <th>
                <p>Description</p>
              </th>
              <th>
                <p>Usage</p>
              </th>
            </tr>
            <tr>
              <td>
                <p>
                  <code>confluence_healthcheck</code>
                </p>
              </td>
              <td>
                <p>Verify Confluence configuration and connectivity</p>
              </td>
              <td>
                <p>Run after setup to ensure everything is working</p>
              </td>
            </tr>
          </tbody>
        </table>
        <ac:structured-macro ac:macro-id="2e43695e-209b-419a-9086-117f2c987a3d" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">Documentation Retrieval</ac:parameter>
          <ac:rich-text-body>
            <table>
              <tbody>
                <tr>
                  <th>
                    <p>Tool</p>
                  </th>
                  <th>
                    <p>Description</p>
                  </th>
                  <th>
                    <p>Parameters</p>
                  </th>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>get_confluence_pages</code>
                    </p>
                  </td>
                  <td>
                    <p>Get pages from a specific Confluence space</p>
                  </td>
                  <td>
                    <p>
                      <code>space_key</code>, <code>limit</code> (default: 50)</p>
                  </td>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>get_confluence_page_by_title</code>
                    </p>
                  </td>
                  <td>
                    <p>Get specific page by title from a space</p>
                  </td>
                  <td>
                    <p>
                      <code>space_key</code>, <code>page_title</code>
                    </p>
                  </td>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>get_space_documentation</code>
                    </p>
                  </td>
                  <td>
                    <p>Get comprehensive space documentation with content</p>
                  </td>
                  <td>
                    <p>
                      <code>space_key</code>, <code>include_content</code> (default: true)</p>
                  </td>
                </tr>
              </tbody>
            </table>
          </ac:rich-text-body>
        </ac:structured-macro>
        <ac:structured-macro ac:macro-id="7a682e49-32c4-46d3-8fd2-0f09815948ba" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">Search &amp; Discovery</ac:parameter>
          <ac:rich-text-body>
            <table>
              <tbody>
                <tr>
                  <th>
                    <p>Tool</p>
                  </th>
                  <th>
                    <p>Description</p>
                  </th>
                  <th>
                    <p>Parameters</p>
                  </th>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>search_confluence</code>
                    </p>
                  </td>
                  <td>
                    <p>Search across Confluence content</p>
                  </td>
                  <td>
                    <p>
                      <code>query</code>, <code>space_key</code> (optional), <code>limit</code> (default: 25)</p>
                  </td>
                </tr>
                <tr>
                  <td>
                    <p>
                      <code>get_confluence_spaces</code>
                    </p>
                  </td>
                  <td>
                    <p>List available Confluence spaces</p>
                  </td>
                  <td>
                    <p>
                      <code>limit</code> (default: 50)</p>
                  </td>
                </tr>
              </tbody>
            </table>
          </ac:rich-text-body>
        </ac:structured-macro>
      </ac:rich-text-body>
    </ac:structured-macro>
  </ac:rich-text-body>
</ac:structured-macro>
<h3>&#55357;&#56523; Resources</h3>
<table>
  <tbody>
    <tr>
      <th>
        <p>Resource</p>
      </th>
      <th>
        <p>Description</p>
      </th>
      <th>
        <p>Usage</p>
      </th>
    </tr>
    <tr>
      <td>
        <p>
          <code>jira://ticket/{ticket_key</code>}</p>
      </td>
      <td>
        <p>Direct JIRA ticket resource access</p>
      </td>
      <td>
        <p>Reference tickets directly in context</p>
      </td>
    </tr>
  </tbody>
</table>
<hr/>
<h2>&#55357;&#56960; Quick Setup Guide</h2>
<ac:structured-macro ac:macro-id="9b7aa69a-befc-49d5-a563-5a7fd1caf420" ac:name="panel" ac:schema-version="1">
  <ac:parameter ac:name="borderColor">#0052cc</ac:parameter>
  <ac:parameter ac:name="bgColor">#f4f5f7</ac:parameter>
  <ac:parameter ac:name="titleBGColor">#deebff</ac:parameter>
  <ac:parameter ac:name="borderStyle">solid</ac:parameter>
  <ac:parameter ac:name="title">Prerequisites</ac:parameter>
  <ac:rich-text-body>
    <ul>
      <li>Python 3.8 or higher</li>
      <li>VSCode IDE</li>
      <li>JIRA instance access with API token</li>
      <li>Bitbucket instance access with authentication token</li>
      <li>Confluence instance access with API credentials</li>
    </ul>
  </ac:rich-text-body>
</ac:structured-macro>
<h3>One-Click Installation</h3>
<ac:structured-macro ac:macro-id="e2c5c17f-2d3a-44f9-a2a0-1dd53c7052e7" ac:name="deck" ac:schema-version="1">
  <ac:parameter ac:name="id">setup-tabs</ac:parameter>
  <ac:rich-text-body>
    <ac:structured-macro ac:macro-id="864572d3-576f-4fe4-8c34-aa88cb37ec31" ac:name="card" ac:schema-version="1">
      <ac:parameter ac:name="label">Windows (PowerShell)</ac:parameter>
      <ac:rich-text-body>
        <ac:structured-macro ac:macro-id="0531cd8c-fcf0-47f1-94db-77322b79ae02" ac:name="code" ac:schema-version="1">
          <ac:parameter ac:name="language">powershell</ac:parameter>
          <ac:parameter ac:name="title">PowerShell Setup</ac:parameter>
          <ac:plain-text-body><![CDATA[# Clone the repository
git clone https://wlstash.wenlin.net/scm/ingn/mcp-server-library.git
cd mcp-server-library

# Run automated setup
.\setup.ps1

# Or with help
.\setup.ps1 -Help

# Force recreate environment
.\setup.ps1 -Force
]]></ac:plain-text-body>
        </ac:structured-macro>
      </ac:rich-text-body>
    </ac:structured-macro>
    <ac:structured-macro ac:macro-id="0f046980-6a5a-4f30-a5de-59bf979fa2cf" ac:name="card" ac:schema-version="1">
      <ac:parameter ac:name="label">Windows (Batch)</ac:parameter>
      <ac:rich-text-body>
        <ac:structured-macro ac:macro-id="bd6b7276-27e7-4d03-9191-66f5f6571b69" ac:name="code" ac:schema-version="1">
          <ac:parameter ac:name="language">batch</ac:parameter>
          <ac:parameter ac:name="title">Batch Setup</ac:parameter>
          <ac:plain-text-body><![CDATA[# Clone the repository
git clone https://wlstash.wenlin.net/scm/ingn/mcp-server-library.git
cd mcp-server-library

# Run automated setup
.\setup.bat
]]></ac:plain-text-body>
        </ac:structured-macro>
      </ac:rich-text-body>
    </ac:structured-macro>
    <ac:structured-macro ac:macro-id="93fe3eb6-1177-45a1-9456-514603156179" ac:name="card" ac:schema-version="1">
      <ac:parameter ac:name="label">macOS/Linux (Bash)</ac:parameter>
      <ac:rich-text-body>
        <ac:structured-macro ac:macro-id="73076bf7-5789-45fb-9491-aae18e6bf1ae" ac:name="code" ac:schema-version="1">
          <ac:parameter ac:name="language">bash</ac:parameter>
          <ac:parameter ac:name="title">Bash Setup</ac:parameter>
          <ac:plain-text-body><![CDATA[# Clone the repository
git clone https://wlstash.wenlin.net/scm/ingn/mcp-server-library.git
cd mcp-server-library

# Make script executable and run
chmod +x setup.sh
./setup.sh
]]></ac:plain-text-body>
        </ac:structured-macro>
      </ac:rich-text-body>
    </ac:structured-macro>
  </ac:rich-text-body>
</ac:structured-macro>
<ac:structured-macro ac:macro-id="3ecf2689-a99a-411f-95d2-8c4a340fbe39" ac:name="panel" ac:schema-version="1">
  <ac:parameter ac:name="borderColor">#36b37e</ac:parameter>
  <ac:parameter ac:name="bgColor">#fff</ac:parameter>
  <ac:parameter ac:name="titleBGColor">#e3fcef</ac:parameter>
  <ac:parameter ac:name="borderStyle">dashed</ac:parameter>
  <ac:parameter ac:name="title">What the Setup Scripts Do</ac:parameter>
  <ac:rich-text-body>
    <p>1. ✅ <strong>Check Python Installation</strong> - Verifies Python 3.8+ is available<br/>2. ✅ <strong>Create Virtual Environment</strong> - Isolates dependencies <br/>3. ✅ <strong>Install Dependencies</strong> - Installs all required packages from <code>requirements.txt</code>
      <br/>4. ✅ <strong>Configure MCP Servers</strong> - Updates VSCode settings automatically for JIRA, Bitbucket, and Confluence<br/>5. ✅ <strong>Provide Next Steps</strong> - Clear instructions for token setup</p>
  </ac:rich-text-body>
</ac:structured-macro>
<hr/>
<h2>&#55357;&#56592; Authentication Setup</h2>
<ac:structured-macro ac:macro-id="163150aa-fb28-482f-b59b-21e965b241ff" ac:name="deck" ac:schema-version="1">
  <ac:parameter ac:name="id">auth-tabs</ac:parameter>
  <ac:rich-text-body>
    <ac:structured-macro ac:macro-id="d6d24304-f600-48f9-a2c1-6e0ba3a9efb0" ac:name="card" ac:schema-version="1">
      <ac:parameter ac:name="label">Step 1: Get API Tokens</ac:parameter>
      <ac:rich-text-body>
        <ac:structured-macro ac:macro-id="db4aa500-68e9-40fd-bfc7-bfa9743edbf8" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">JIRA API Token</ac:parameter>
          <ac:rich-text-body>
            <p>1. Go to your JIRA instance<br/>2. Click your profile picture → <strong>Account Settings</strong>
              <br/>3. Navigate to <strong>Security</strong> → <strong>Create and manage API tokens</strong>
              <br/>4. Click <strong>Create API token</strong>
              <br/>5. Copy the generated token (save it securely!)</p>
          </ac:rich-text-body>
        </ac:structured-macro>
        <ac:structured-macro ac:macro-id="d04dfc49-f25f-4d7d-afbc-265a03031e5b" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">Bitbucket Authentication Token</ac:parameter>
          <ac:rich-text-body>
            <p>1. Go to your Bitbucket instance<br/>2. Navigate to <strong>Account Settings</strong> → <strong>Personal Access Tokens</strong>
              <br/>3. Click <strong>Create Token</strong>
              <br/>4. Set appropriate permissions (repos, pull requests, etc.)<br/>5. Copy the generated token (save it securely!)</p>
          </ac:rich-text-body>
        </ac:structured-macro>
        <ac:structured-macro ac:macro-id="3ec27f9b-5cde-4b7b-a945-24b007a28039" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">Confluence Authentication Token</ac:parameter>
          <ac:rich-text-body>
            <p>1. Go to your Confluence instance<br/>2. Click your profile picture → <strong>Account Settings</strong>
              <br/>3. Navigate to <strong>Security</strong> → <strong>Create and manage API tokens</strong>
              <br/>4. Click <strong>Create API token</strong>
              <br/>5. Copy the generated token (save it securely!)</p>
          </ac:rich-text-body>
        </ac:structured-macro>
      </ac:rich-text-body>
    </ac:structured-macro>
    <ac:structured-macro ac:macro-id="f09922ca-11ad-4d58-9307-bad383e799dc" ac:name="card" ac:schema-version="1">
      <ac:parameter ac:name="label">Step 2: Configure Tokens</ac:parameter>
      <ac:rich-text-body>
        <ac:structured-macro ac:macro-id="a42c050f-6c64-4234-9a7d-d70486f1c800" ac:name="panel" ac:schema-version="1">
          <ac:parameter ac:name="borderColor">#ff5630</ac:parameter>
          <ac:parameter ac:name="bgColor">#fff</ac:parameter>
          <ac:parameter ac:name="titleBGColor">#ffebe6</ac:parameter>
          <ac:parameter ac:name="borderStyle">solid</ac:parameter>
          <ac:parameter ac:name="title">Using VSCode/Cursor Settings (Recommended)</ac:parameter>
          <ac:rich-text-body>
            <p>1. Open VSCode<br/>2. Press <code>Ctrl+Shift+P</code> (or <code>Cmd+Shift+P</code> on Mac)<br/>3. Type "Open User Settings (JSON)" and select it<br/>4. Find or add the MCP configuration:</p>
          </ac:rich-text-body>
        </ac:structured-macro>
        <ac:structured-macro ac:macro-id="2c4eae8f-8681-4037-b905-51154efa0629" ac:name="code" ac:schema-version="1">
          <ac:parameter ac:name="language">json</ac:parameter>
          <ac:parameter ac:name="title">VSCode Settings Configuration</ac:parameter>
          <ac:plain-text-body><![CDATA[{
  "mcp": {
    "servers": {
      "jira-mcp-server": {
        "type": "stdio",
        "command": "/path/to/your/.venv/Scripts/python.exe",
        "args": ["/path/to/your/servers/jira_mcp_server.py"],
        "env": {
          "JIRA_AUTH_TOKEN": "your-secure-auth-token",
          "JIRA_BASE_URL": "https://wljira.wenlin.net"
        }
      },
      "bitbucket-mcp-server": {
        "type": "stdio",
        "command": "/path/to/your/.venv/Scripts/python.exe",
        "args": ["/path/to/your/servers/bitbucket_server.py"],
        "env": {
          "BITBUCKET_AUTH_TOKEN": "your-bitbucket-token-here",
          "BITBUCKET_BASE_URL": "http://wlstash.wenlin.net"
        }
      },
      "confluence-mcp-server": {
        "type": "stdio",
        "command": "/path/to/your/.venv/Scripts/python.exe",
        "args": ["/path/to/your/servers/confluence_server.py"],
        "env": {
          "CONFLUENCE_USERNAME": "your-confluence-username",
          "CONFLUENCE_API_KEY": "your-confluence-api-token",
          "CONFLUENCE_BASE_URL": "https://wenlin.atlassian.net"
        }
      }
    }
  }
}
]]></ac:plain-text-body>
        </ac:structured-macro>
      </ac:rich-text-body>
    </ac:structured-macro>
    <ac:structured-macro ac:macro-id="c6bedb15-372a-4f42-933d-582f2a8a644d" ac:name="card" ac:schema-version="1">
      <ac:parameter ac:name="label">Step 3: Verify Setup</ac:parameter>
      <ac:rich-text-body>
        <ac:structured-macro ac:macro-id="05f698c4-141b-492c-a9f9-e288139b471b" ac:name="panel" ac:schema-version="1">
          <ac:parameter ac:name="borderColor">#36b37e</ac:parameter>
          <ac:parameter ac:name="bgColor">#fff</ac:parameter>
          <ac:parameter ac:name="titleBGColor">#e3fcef</ac:parameter>
          <ac:parameter ac:name="borderStyle">solid</ac:parameter>
          <ac:parameter ac:name="title">Verification Steps</ac:parameter>
          <ac:rich-text-body>
            <p>1. Restart VSCode<br/>2. Use the <code>healthcheck</code> tool to verify JIRA configuration<br/>3. Use the <code>test_connection</code> tool to test JIRA authentication<br/>4. Use the <code>bitbucket_healthcheck</code> tool to verify Bitbucket configuration<br/>5. Use the <code>confluence_healthcheck</code> tool to verify Confluence configuration</p>
          </ac:rich-text-body>
        </ac:structured-macro>
      </ac:rich-text-body>
    </ac:structured-macro>
  </ac:rich-text-body>
</ac:structured-macro>
<hr/>
<h2>&#55357;&#56534; Usage Examples</h2>
<ac:structured-macro ac:macro-id="25f59d93-bfd2-4e84-a7bc-9ce5e04e1e28" ac:name="deck" ac:schema-version="1">
  <ac:parameter ac:name="id">usage-tabs</ac:parameter>
  <ac:rich-text-body>
    <ac:structured-macro ac:macro-id="8f0d8485-85de-4e67-988b-d3e918e45816" ac:name="card" ac:schema-version="1">
      <ac:parameter ac:name="label">JIRA Examples</ac:parameter>
      <ac:rich-text-body>
        <ac:structured-macro ac:macro-id="5f731a80-c9e3-4c89-8a94-ad626d0d8551" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">Basic Health Check</ac:parameter>
          <ac:rich-text-body>
            <ac:structured-macro ac:macro-id="7e34fbff-f454-4035-a394-9418b1acd9ac" ac:name="panel" ac:schema-version="1">
              <ac:parameter ac:name="borderColor">#0052cc</ac:parameter>
              <ac:parameter ac:name="bgColor">#fff</ac:parameter>
              <ac:parameter ac:name="titleBGColor">#deebff</ac:parameter>
              <ac:parameter ac:name="borderStyle">dashed</ac:parameter>
              <ac:parameter ac:name="title">Health Check</ac:parameter>
              <ac:rich-text-body>
                <p>Run the healthcheck tool to verify your JIRA setup:</p>
                <ul>
                  <li>Tool: <code>healthcheck</code>
                  </li>
                  <li>Expected: Configuration status and setup guidance</li>
                </ul>
              </ac:rich-text-body>
            </ac:structured-macro>
          </ac:rich-text-body>
        </ac:structured-macro>
        <ac:structured-macro ac:macro-id="b4fea4fc-9fd2-4063-b5a8-72b08426da63" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">Get Your Active Work</ac:parameter>
          <ac:rich-text-body>
            <ac:structured-macro ac:macro-id="a0dc9c2d-0f46-45c6-8011-83a8d0ca2958" ac:name="panel" ac:schema-version="1">
              <ac:parameter ac:name="borderColor">#0052cc</ac:parameter>
              <ac:parameter ac:name="bgColor">#fff</ac:parameter>
              <ac:parameter ac:name="titleBGColor">#deebff</ac:parameter>
              <ac:parameter ac:name="borderStyle">dashed</ac:parameter>
              <ac:parameter ac:name="title">Active Work</ac:parameter>
              <ac:rich-text-body>
                <p>Find all tickets assigned to you:</p>
                <ul>
                  <li>Tool: <code>get_my_active_work</code>
                  </li>
                </ul>
              </ac:rich-text-body>
            </ac:structured-macro>
          </ac:rich-text-body>
        </ac:structured-macro>
        <ac:structured-macro ac:macro-id="996d7539-f4fe-4b14-9178-b778e110ec8c" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">Create Code Review Task</ac:parameter>
          <ac:rich-text-body>
            <ac:structured-macro ac:macro-id="249d4f63-3ba9-4b1c-8830-77cdfdf24984" ac:name="panel" ac:schema-version="1">
              <ac:parameter ac:name="borderColor">#0052cc</ac:parameter>
              <ac:parameter ac:name="bgColor">#fff</ac:parameter>
              <ac:parameter ac:name="titleBGColor">#deebff</ac:parameter>
              <ac:parameter ac:name="borderStyle">dashed</ac:parameter>
              <ac:parameter ac:name="title">Code Review</ac:parameter>
              <ac:rich-text-body>
                <p>Create a code review task:</p>
                <ul>
                  <li>Tool: <code>create_review_task</code>
                  </li>
                  <li>Parameters:<ul>
                      <li>
                        <code>parent_key</code>: "PROD-1234"</li>
                      <li>
                        <code>title</code>: "Code Review: OAuth2 Integration"</li>
                      <li>
                        <code>description</code>: "Review the new OAuth2 authentication implementation"</li>
                    </ul>
                  </li>
                </ul>
              </ac:rich-text-body>
            </ac:structured-macro>
          </ac:rich-text-body>
        </ac:structured-macro>
        <ac:structured-macro ac:macro-id="2c694342-01f5-4f63-8ef8-a709737bf198" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">Sprint Progress Monitoring</ac:parameter>
          <ac:rich-text-body>
            <ac:structured-macro ac:macro-id="713eaeda-44b4-47e3-a5c2-7dceab627a90" ac:name="panel" ac:schema-version="1">
              <ac:parameter ac:name="borderColor">#0052cc</ac:parameter>
              <ac:parameter ac:name="bgColor">#fff</ac:parameter>
              <ac:parameter ac:name="titleBGColor">#deebff</ac:parameter>
              <ac:parameter ac:name="borderStyle">dashed</ac:parameter>
              <ac:parameter ac:name="title">Sprint Burndown</ac:parameter>
              <ac:rich-text-body>
                <p>Check current sprint burndown:</p>
                <ul>
                  <li>Tool: <code>get_sprint_burndown</code>
                  </li>
                  <li>Parameters:<ul>
                      <li>
                        <code>project_key</code>: "PROD"</li>
                    </ul>
                  </li>
                </ul>
              </ac:rich-text-body>
            </ac:structured-macro>
          </ac:rich-text-body>
        </ac:structured-macro>
        <ac:structured-macro ac:macro-id="cdd8b8b6-fe14-4b83-b495-efdc577dd63e" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">Custom JQL Search</ac:parameter>
          <ac:rich-text-body>
            <ac:structured-macro ac:macro-id="9688dcc9-28f3-49a3-82a9-f2189400fcd3" ac:name="panel" ac:schema-version="1">
              <ac:parameter ac:name="borderColor">#0052cc</ac:parameter>
              <ac:parameter ac:name="bgColor">#fff</ac:parameter>
              <ac:parameter ac:name="titleBGColor">#deebff</ac:parameter>
              <ac:parameter ac:name="borderStyle">dashed</ac:parameter>
              <ac:parameter ac:name="title">Custom Search</ac:parameter>
              <ac:rich-text-body>
                <p>Execute custom JQL queries:</p>
                <ul>
                  <li>Tool: <code>search_jira_custom</code>
                  </li>
                  <li>Parameters:<ul>
                      <li>
                        <code>jql_query</code>: "project = PROD AND assignee = currentUser() AND status = 'In Progress'"</li>
                      <li>
                        <code>max_results</code>: 25</li>
                    </ul>
                  </li>
                </ul>
              </ac:rich-text-body>
            </ac:structured-macro>
          </ac:rich-text-body>
        </ac:structured-macro>
      </ac:rich-text-body>
    </ac:structured-macro>
    <ac:structured-macro ac:macro-id="9f488b40-0ab8-495a-a562-bfef56ee681c" ac:name="card" ac:schema-version="1">
      <ac:parameter ac:name="label">Bitbucket Examples</ac:parameter>
      <ac:rich-text-body>
        <ac:structured-macro ac:macro-id="05715f44-114b-45c9-8fae-e2951581d7e6" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">Bitbucket Health Check</ac:parameter>
          <ac:rich-text-body>
            <ac:structured-macro ac:macro-id="106a20f1-9c81-48e3-ba8d-4b4cc35ae595" ac:name="panel" ac:schema-version="1">
              <ac:parameter ac:name="borderColor">#0747a6</ac:parameter>
              <ac:parameter ac:name="bgColor">#fff</ac:parameter>
              <ac:parameter ac:name="titleBGColor">#deebff</ac:parameter>
              <ac:parameter ac:name="borderStyle">dashed</ac:parameter>
              <ac:parameter ac:name="title">Health Check</ac:parameter>
              <ac:rich-text-body>
                <p>Verify Bitbucket connectivity:</p>
                <ul>
                  <li>Tool: <code>bitbucket_healthcheck</code>
                  </li>
                  <li>Expected: Connection status and configuration info</li>
                </ul>
              </ac:rich-text-body>
            </ac:structured-macro>
          </ac:rich-text-body>
        </ac:structured-macro>
        <ac:structured-macro ac:macro-id="f6cee4f4-bd0f-473b-9b24-e0f110653672" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">Get Pull Request Details</ac:parameter>
          <ac:rich-text-body>
            <ac:structured-macro ac:macro-id="b7bbe0a4-3625-4a07-9f00-ae9ac4e3750a" ac:name="panel" ac:schema-version="1">
              <ac:parameter ac:name="borderColor">#0747a6</ac:parameter>
              <ac:parameter ac:name="bgColor">#fff</ac:parameter>
              <ac:parameter ac:name="titleBGColor">#deebff</ac:parameter>
              <ac:parameter ac:name="borderStyle">dashed</ac:parameter>
              <ac:parameter ac:name="title">PR Analysis</ac:parameter>
              <ac:rich-text-body>
                <p>Analyze a specific pull request:</p>
                <ul>
                  <li>Tool: <code>get_pr_details</code>
                  </li>
                  <li>Parameters:<ul>
                      <li>
                        <code>pr_link</code>: "https://wlstash.wenlin.net/projects/INGN/repos/ingn_api/pull-requests/866/overview"</li>
                    </ul>
                  </li>
                  <li>Returns: PR data, diff content, author, reviewers, and metadata</li>
                </ul>
              </ac:rich-text-body>
            </ac:structured-macro>
          </ac:rich-text-body>
        </ac:structured-macro>
        <ac:structured-macro ac:macro-id="13322b3d-b3f5-4343-98c2-2bbc07471bd4" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">Add PR Comment</ac:parameter>
          <ac:rich-text-body>
            <ac:structured-macro ac:macro-id="a0346596-c171-4467-a779-d231950e1132" ac:name="panel" ac:schema-version="1">
              <ac:parameter ac:name="borderColor">#0747a6</ac:parameter>
              <ac:parameter ac:name="bgColor">#fff</ac:parameter>
              <ac:parameter ac:name="titleBGColor">#deebff</ac:parameter>
              <ac:parameter ac:name="borderStyle">dashed</ac:parameter>
              <ac:parameter ac:name="title">PR Feedback</ac:parameter>
              <ac:rich-text-body>
                <p>Provide feedback on a pull request:</p>
                <ul>
                  <li>Tool: <code>add_pr_comment</code>
                  </li>
                  <li>Parameters:<ul>
                      <li>
                        <code>pr_link</code>: "https://wlstash.wenlin.net/projects/INGN/repos/ingn_api/pull-requests/866"</li>
                      <li>
                        <code>comment_text</code>: "Great implementation! Consider adding unit tests for the new authentication flow."</li>
                      <li>
                        <code>line_comment</code>: "auth.py:45" (optional, for line-specific comments)</li>
                    </ul>
                  </li>
                </ul>
              </ac:rich-text-body>
            </ac:structured-macro>
          </ac:rich-text-body>
        </ac:structured-macro>
        <ac:structured-macro ac:macro-id="7dbd4c6d-2661-4f88-a911-cd4876a2ae31" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">Create Pull Request</ac:parameter>
          <ac:rich-text-body>
            <ac:structured-macro ac:macro-id="21e5512a-52f8-4e96-a969-593e3345d2af" ac:name="panel" ac:schema-version="1">
              <ac:parameter ac:name="borderColor">#0747a6</ac:parameter>
              <ac:parameter ac:name="bgColor">#fff</ac:parameter>
              <ac:parameter ac:name="titleBGColor">#deebff</ac:parameter>
              <ac:parameter ac:name="borderStyle">dashed</ac:parameter>
              <ac:parameter ac:name="title">New PR</ac:parameter>
              <ac:rich-text-body>
                <p>Create a new pull request:</p>
                <ul>
                  <li>Tool: <code>create_pull_request</code>
                  </li>
                  <li>Parameters:<ul>
                      <li>
                        <code>workspace</code>: "INGN"</li>
                      <li>
                        <code>repo_slug</code>: "main-api"</li>
                      <li>
                        <code>source_branch</code>: "feature/oauth2-integration"</li>
                      <li>
                        <code>target_branch</code>: "develop"</li>
                      <li>
                        <code>title</code>: "INGN-123: Implement OAuth2 Authentication"</li>
                      <li>
                        <code>description</code>: "Adds OAuth2 authentication support with JWT tokens"</li>
                      <li>
                        <code>reviewers</code>: <ac:link>
                          <ri:page ri:content-title="&quot;team-lead&quot;, &quot;senior-dev&quot;" ri:space-key="~rtalrej"/>
                        </ac:link>
                      </li>
                    </ul>
                  </li>
                </ul>
              </ac:rich-text-body>
            </ac:structured-macro>
          </ac:rich-text-body>
        </ac:structured-macro>
      </ac:rich-text-body>
    </ac:structured-macro>
    <ac:structured-macro ac:macro-id="e9d6980d-0a11-459c-b1c0-1e7810c4e04b" ac:name="card" ac:schema-version="1">
      <ac:parameter ac:name="label">Confluence Examples</ac:parameter>
      <ac:rich-text-body>
        <ac:structured-macro ac:macro-id="f266901b-607c-4851-b734-02d624c57776" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">Confluence Health Check</ac:parameter>
          <ac:rich-text-body>
            <ac:structured-macro ac:macro-id="02b36994-6e00-47ec-9b83-40356606344c" ac:name="panel" ac:schema-version="1">
              <ac:parameter ac:name="borderColor">#172b4d</ac:parameter>
              <ac:parameter ac:name="bgColor">#fff</ac:parameter>
              <ac:parameter ac:name="titleBGColor">#f4f5f7</ac:parameter>
              <ac:parameter ac:name="borderStyle">dashed</ac:parameter>
              <ac:parameter ac:name="title">Health Check</ac:parameter>
              <ac:rich-text-body>
                <p>Verify Confluence connectivity:</p>
                <ul>
                  <li>Tool: <code>confluence_healthcheck</code>
                  </li>
                  <li>Expected: Connection status and configuration info</li>
                </ul>
              </ac:rich-text-body>
            </ac:structured-macro>
          </ac:rich-text-body>
        </ac:structured-macro>
        <ac:structured-macro ac:macro-id="fee65891-c895-42d0-b6af-7f436044f265" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">Search Documentation</ac:parameter>
          <ac:rich-text-body>
            <ac:structured-macro ac:macro-id="c8b674e5-80c0-4175-88fa-28a31dfcb2ce" ac:name="panel" ac:schema-version="1">
              <ac:parameter ac:name="borderColor">#172b4d</ac:parameter>
              <ac:parameter ac:name="bgColor">#fff</ac:parameter>
              <ac:parameter ac:name="titleBGColor">#f4f5f7</ac:parameter>
              <ac:parameter ac:name="borderStyle">dashed</ac:parameter>
              <ac:parameter ac:name="title">Documentation Search</ac:parameter>
              <ac:rich-text-body>
                <p>Find relevant documentation:</p>
                <ul>
                  <li>Tool: <code>search_confluence</code>
                  </li>
                  <li>Parameters:<ul>
                      <li>
                        <code>query</code>: "OAuth2 authentication"</li>
                      <li>
                        <code>space_key</code>: "DEV" (optional)</li>
                      <li>
                        <code>limit</code>: 10</li>
                    </ul>
                  </li>
                  <li>Returns: Matching pages with titles, URLs, and excerpts</li>
                </ul>
              </ac:rich-text-body>
            </ac:structured-macro>
          </ac:rich-text-body>
        </ac:structured-macro>
        <ac:structured-macro ac:macro-id="8cc7af04-5d68-4554-aff0-a719f6c8cbe3" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">Get Space Pages</ac:parameter>
          <ac:rich-text-body>
            <ac:structured-macro ac:macro-id="13161549-4e57-4e93-9d3f-51c25f2ad80b" ac:name="panel" ac:schema-version="1">
              <ac:parameter ac:name="borderColor">#172b4d</ac:parameter>
              <ac:parameter ac:name="bgColor">#fff</ac:parameter>
              <ac:parameter ac:name="titleBGColor">#f4f5f7</ac:parameter>
              <ac:parameter ac:name="borderStyle">dashed</ac:parameter>
              <ac:parameter ac:name="title">Space Content</ac:parameter>
              <ac:rich-text-body>
                <p>List all pages in a space:</p>
                <ul>
                  <li>Tool: <code>get_confluence_pages</code>
                  </li>
                  <li>Parameters:<ul>
                      <li>
                        <code>space_key</code>: "PROD"</li>
                      <li>
                        <code>limit</code>: 25</li>
                    </ul>
                  </li>
                  <li>Returns: Page titles, URLs, and basic metadata</li>
                </ul>
              </ac:rich-text-body>
            </ac:structured-macro>
          </ac:rich-text-body>
        </ac:structured-macro>
        <ac:structured-macro ac:macro-id="3247dee3-5bdc-4199-a794-961511ca2cb3" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">Get Specific Page</ac:parameter>
          <ac:rich-text-body>
            <ac:structured-macro ac:macro-id="b42eec32-eccc-4c7e-a836-ca67065f08b6" ac:name="panel" ac:schema-version="1">
              <ac:parameter ac:name="borderColor">#172b4d</ac:parameter>
              <ac:parameter ac:name="bgColor">#fff</ac:parameter>
              <ac:parameter ac:name="titleBGColor">#f4f5f7</ac:parameter>
              <ac:parameter ac:name="borderStyle">dashed</ac:parameter>
              <ac:parameter ac:name="title">Page Retrieval</ac:parameter>
              <ac:rich-text-body>
                <p>Retrieve a specific documentation page:</p>
                <ul>
                  <li>Tool: <code>get_confluence_page_by_title</code>
                  </li>
                  <li>Parameters:<ul>
                      <li>
                        <code>space_key</code>: "DEV"</li>
                      <li>
                        <code>page_title</code>: "API Documentation"</li>
                    </ul>
                  </li>
                  <li>Returns: Full page content converted to markdown</li>
                </ul>
              </ac:rich-text-body>
            </ac:structured-macro>
          </ac:rich-text-body>
        </ac:structured-macro>
      </ac:rich-text-body>
    </ac:structured-macro>
  </ac:rich-text-body>
</ac:structured-macro>
<h3>Integrated Workflows</h3>
<ac:structured-macro ac:macro-id="a2854144-6cfd-4a72-b06b-98a6781df7aa" ac:name="deck" ac:schema-version="1">
  <ac:parameter ac:name="id">workflow-tabs</ac:parameter>
  <ac:rich-text-body>
    <ac:structured-macro ac:macro-id="91f8cd80-9591-4a73-997b-2e49dfc6a67f" ac:name="card" ac:schema-version="1">
      <ac:parameter ac:name="label">Feature Development</ac:parameter>
      <ac:rich-text-body>
        <ac:structured-macro ac:macro-id="f17c2987-b459-4c75-9882-c8d16cc20241" ac:name="panel" ac:schema-version="1">
          <ac:parameter ac:name="borderColor">#36b37e</ac:parameter>
          <ac:parameter ac:name="bgColor">#fff</ac:parameter>
          <ac:parameter ac:name="titleBGColor">#e3fcef</ac:parameter>
          <ac:parameter ac:name="borderStyle">solid</ac:parameter>
          <ac:parameter ac:name="title">Feature Development Workflow</ac:parameter>
          <ac:rich-text-body>
            <p>1. JIRA: <code>get_my_active_work</code> - Check assigned tickets<br/>2. JIRA: <code>get_ticket_details</code> - Get specific ticket info<br/>3. Confluence: <code>search_confluence</code> - Find relevant documentation<br/>4. Bitbucket: <code>get_repository_branches</code> - Check branch status<br/>5. Bitbucket: <code>create_pull_request</code> - Submit code for review<br/>6. JIRA: <code>create_review_task</code> - Create review task in JIRA</p>
          </ac:rich-text-body>
        </ac:structured-macro>
      </ac:rich-text-body>
    </ac:structured-macro>
    <ac:structured-macro ac:macro-id="fe675442-9642-470e-b3f8-caf439b30e14" ac:name="card" ac:schema-version="1">
      <ac:parameter ac:name="label">Documentation-Driven Development</ac:parameter>
      <ac:rich-text-body>
        <ac:structured-macro ac:macro-id="91de9b15-2545-4066-a098-7f3d4be6dfd4" ac:name="panel" ac:schema-version="1">
          <ac:parameter ac:name="borderColor">#36b37e</ac:parameter>
          <ac:parameter ac:name="bgColor">#fff</ac:parameter>
          <ac:parameter ac:name="titleBGColor">#e3fcef</ac:parameter>
          <ac:parameter ac:name="borderStyle">solid</ac:parameter>
          <ac:parameter ac:name="title">Documentation-Driven Development</ac:parameter>
          <ac:rich-text-body>
            <p>1. Confluence: <code>search_confluence</code> - Find existing documentation<br/>2. Confluence: <code>get_confluence_page_by_title</code> - Get detailed specs<br/>3. JIRA: <code>create_user_story</code> - Create development tasks<br/>4. Bitbucket: <code>create_pull_request</code> - Implement features<br/>5. Confluence: Update documentation with implementation details</p>
          </ac:rich-text-body>
        </ac:structured-macro>
      </ac:rich-text-body>
    </ac:structured-macro>
    <ac:structured-macro ac:macro-id="cd964b2d-97e2-4a37-93f7-ce36b354f4b0" ac:name="card" ac:schema-version="1">
      <ac:parameter ac:name="label">Code Review Process</ac:parameter>
      <ac:rich-text-body>
        <ac:structured-macro ac:macro-id="cd90deea-930c-4997-ab03-2e5c94bab619" ac:name="panel" ac:schema-version="1">
          <ac:parameter ac:name="borderColor">#36b37e</ac:parameter>
          <ac:parameter ac:name="bgColor">#fff</ac:parameter>
          <ac:parameter ac:name="titleBGColor">#e3fcef</ac:parameter>
          <ac:parameter ac:name="borderStyle">solid</ac:parameter>
          <ac:parameter ac:name="title">Code Review Process</ac:parameter>
          <ac:rich-text-body>
            <p>1. Bitbucket: <code>get_reviewed_prs</code> - Find PRs to review<br/>2. Bitbucket: <code>get_pr_details</code> - Analyze changes and diff<br/>3. Confluence: <code>search_confluence</code> - Check related documentation<br/>4. Bitbucket: <code>add_pr_comment</code> - Provide structured feedback<br/>5. Bitbucket: <code>get_pr_activities</code> - Check discussion history<br/>6. JIRA: update ticket status after review completion</p>
          </ac:rich-text-body>
        </ac:structured-macro>
      </ac:rich-text-body>
    </ac:structured-macro>
  </ac:rich-text-body>
</ac:structured-macro>
<hr/>
<h2>⚙️ Configuration Options</h2>
<ac:structured-macro ac:macro-id="278506f9-0ed3-4c31-a1cd-5e2128d463e8" ac:name="deck" ac:schema-version="1">
  <ac:parameter ac:name="id">config-tabs</ac:parameter>
  <ac:rich-text-body>
    <ac:structured-macro ac:macro-id="5ac1dcea-58ad-4a98-bec7-009da87ec149" ac:name="card" ac:schema-version="1">
      <ac:parameter ac:name="label">Environment Variables</ac:parameter>
      <ac:rich-text-body>
        <ac:structured-macro ac:macro-id="7b156e9d-64d9-4235-bca2-36c7de2a7d3f" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">JIRA Configuration</ac:parameter>
          <ac:rich-text-body>
            <ac:structured-macro ac:macro-id="91d462cc-7850-4acb-a33b-4170efa7d5df" ac:name="code" ac:schema-version="1">
              <ac:parameter ac:name="language">bash</ac:parameter>
              <ac:parameter ac:name="title">JIRA Environment Variables</ac:parameter>
              <ac:plain-text-body><![CDATA[export JIRA_AUTH_TOKEN=your-secure-auth-token
export JIRA_BASE_URL=https://wljira.wenlin.net
]]></ac:plain-text-body>
            </ac:structured-macro>
          </ac:rich-text-body>
        </ac:structured-macro>
        <ac:structured-macro ac:macro-id="bf673a55-f342-417e-966e-21394e0ad871" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">Bitbucket Configuration</ac:parameter>
          <ac:rich-text-body>
            <ac:structured-macro ac:macro-id="21664c10-9777-4616-8606-c9ca4b1417ce" ac:name="code" ac:schema-version="1">
              <ac:parameter ac:name="language">bash</ac:parameter>
              <ac:parameter ac:name="title">Bitbucket Environment Variables</ac:parameter>
              <ac:plain-text-body><![CDATA[BITBUCKET_AUTH_TOKEN=your-bitbucket-token
BITBUCKET_BASE_URL=http://wlstash.wenlin.net
]]></ac:plain-text-body>
            </ac:structured-macro>
          </ac:rich-text-body>
        </ac:structured-macro>
        <ac:structured-macro ac:macro-id="aa5beefd-8d3e-4ac7-8e23-7aa391ceb228" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">Confluence Configuration</ac:parameter>
          <ac:rich-text-body>
            <ac:structured-macro ac:macro-id="2dded9b5-1358-45ce-be73-9d6da8a9cb9b" ac:name="code" ac:schema-version="1">
              <ac:parameter ac:name="language">bash</ac:parameter>
              <ac:parameter ac:name="title">Confluence Environment Variables</ac:parameter>
              <ac:plain-text-body><![CDATA[CONFLUENCE_USERNAME=your-confluence-username
CONFLUENCE_API_KEY=your-confluence-api-token
CONFLUENCE_BASE_URL=https://wenlin.atlassian.net
]]></ac:plain-text-body>
            </ac:structured-macro>
          </ac:rich-text-body>
        </ac:structured-macro>
      </ac:rich-text-body>
    </ac:structured-macro>
    <ac:structured-macro ac:macro-id="a07fd5f7-f09b-4930-a677-297e9240c6f0" ac:name="card" ac:schema-version="1">
      <ac:parameter ac:name="label">Default Project Configuration</ac:parameter>
      <ac:rich-text-body>
        <ac:structured-macro ac:macro-id="fbeb4270-d676-4895-ab94-b5d1b40596f5" ac:name="panel" ac:schema-version="1">
          <ac:parameter ac:name="borderColor">#ff5630</ac:parameter>
          <ac:parameter ac:name="bgColor">#fff</ac:parameter>
          <ac:parameter ac:name="titleBGColor">#ffebe6</ac:parameter>
          <ac:parameter ac:name="borderStyle">dashed</ac:parameter>
          <ac:parameter ac:name="title">Project Defaults</ac:parameter>
          <ac:rich-text-body>
            <p>The JIRA server uses <code>DEFAULT_PROJECT_KEY</code> as the fallback project for tools that don't specify a project. This can be configured per-environment for different teams or projects.</p>
          </ac:rich-text-body>
        </ac:structured-macro>
      </ac:rich-text-body>
    </ac:structured-macro>
  </ac:rich-text-body>
</ac:structured-macro>
<hr/>
<h2>&#55357;&#56615; Troubleshooting</h2>
<ac:structured-macro ac:macro-id="51c52402-c92a-4330-9b44-1c5d08a6a88b" ac:name="deck" ac:schema-version="1">
  <ac:parameter ac:name="id">troubleshooting-tabs</ac:parameter>
  <ac:rich-text-body>
    <ac:structured-macro ac:macro-id="392638e1-c84e-4405-abec-e932107652df" ac:name="card" ac:schema-version="1">
      <ac:parameter ac:name="label">Common Issues</ac:parameter>
      <ac:rich-text-body>
        <ac:structured-macro ac:macro-id="5eac051f-0de0-4712-b8a2-da7f84d57639" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">JIRA Issues</ac:parameter>
          <ac:rich-text-body>
            <ac:structured-macro ac:macro-id="4cbde19a-45cc-4cb8-b474-e24b07369d3b" ac:name="panel" ac:schema-version="1">
              <ac:parameter ac:name="borderColor">#ff5630</ac:parameter>
              <ac:parameter ac:name="bgColor">#fff</ac:parameter>
              <ac:parameter ac:name="titleBGColor">#ffebe6</ac:parameter>
              <ac:parameter ac:name="borderStyle">solid</ac:parameter>
              <ac:parameter ac:name="title">JIRA Troubleshooting</ac:parameter>
              <ac:rich-text-body>
                <ul>
                  <li>
                    <strong>"Authentication failed"</strong>: Verify JIRA API token and username</li>
                  <li>
                    <strong>"Project not found"</strong>: Check project key and permissions</li>
                  <li>
                    <strong>"Connection timeout"</strong>: Verify JIRA base URL and network connectivity</li>
                </ul>
              </ac:rich-text-body>
            </ac:structured-macro>
          </ac:rich-text-body>
        </ac:structured-macro>
        <ac:structured-macro ac:macro-id="30a5ae51-c658-4da5-bdb7-8e80fa982b08" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">Bitbucket Issues</ac:parameter>
          <ac:rich-text-body>
            <ac:structured-macro ac:macro-id="80c06090-3d7f-4b90-92f9-0cfde00c5e3f" ac:name="panel" ac:schema-version="1">
              <ac:parameter ac:name="borderColor">#ff5630</ac:parameter>
              <ac:parameter ac:name="bgColor">#fff</ac:parameter>
              <ac:parameter ac:name="titleBGColor">#ffebe6</ac:parameter>
              <ac:parameter ac:name="borderStyle">solid</ac:parameter>
              <ac:parameter ac:name="title">Bitbucket Troubleshooting</ac:parameter>
              <ac:rich-text-body>
                <ul>
                  <li>
                    <strong>"PR link invalid"</strong>: Ensure full PR URL format is used</li>
                  <li>
                    <strong>"Repository access denied"</strong>: Check repository permissions and auth token</li>
                  <li>
                    <strong>"Branch not found"</strong>: Verify branch names and repository access</li>
                </ul>
              </ac:rich-text-body>
            </ac:structured-macro>
          </ac:rich-text-body>
        </ac:structured-macro>
        <ac:structured-macro ac:macro-id="a6e9dd2f-4da7-4122-83a2-0118a01edf26" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">Confluence Issues</ac:parameter>
          <ac:rich-text-body>
            <ac:structured-macro ac:macro-id="626cd3c1-df8f-45f7-8531-9bdc42606c89" ac:name="panel" ac:schema-version="1">
              <ac:parameter ac:name="borderColor">#ff5630</ac:parameter>
              <ac:parameter ac:name="bgColor">#fff</ac:parameter>
              <ac:parameter ac:name="titleBGColor">#ffebe6</ac:parameter>
              <ac:parameter ac:name="borderStyle">solid</ac:parameter>
              <ac:parameter ac:name="title">Confluence Troubleshooting</ac:parameter>
              <ac:rich-text-body>
                <ul>
                  <li>
                    <strong>"Authentication failed"</strong>: Verify Confluence username and API token</li>
                  <li>
                    <strong>"Space not found"</strong>: Check space key and permissions</li>
                  <li>
                    <strong>"Page not found"</strong>: Verify page title and space access</li>
                </ul>
              </ac:rich-text-body>
            </ac:structured-macro>
          </ac:rich-text-body>
        </ac:structured-macro>
        <ac:structured-macro ac:macro-id="1582328a-de69-45b8-904c-065dbb97d69e" ac:name="expand" ac:schema-version="1">
          <ac:parameter ac:name="title">General Issues</ac:parameter>
          <ac:rich-text-body>
            <ac:structured-macro ac:macro-id="242e6ecd-fbdc-4707-86c2-6ecc8c1c7d36" ac:name="panel" ac:schema-version="1">
              <ac:parameter ac:name="borderColor">#ff5630</ac:parameter>
              <ac:parameter ac:name="bgColor">#fff</ac:parameter>
              <ac:parameter ac:name="titleBGColor">#ffebe6</ac:parameter>
              <ac:parameter ac:name="borderStyle">solid</ac:parameter>
              <ac:parameter ac:name="title">General Troubleshooting</ac:parameter>
              <ac:rich-text-body>
                <ul>
                  <li>
                    <strong>"Python not found"</strong>: Install Python 3.8+ and add to PATH</li>
                  <li>
                    <strong>"Module not found"</strong>: Ensure virtual environment is activated and dependencies installed</li>
                  <li>
                    <strong>"Settings not applied"</strong>: Restart IDE after configuration changes</li>
                </ul>
              </ac:rich-text-body>
            </ac:structured-macro>
          </ac:rich-text-body>
        </ac:structured-macro>
      </ac:rich-text-body>
    </ac:structured-macro>
    <ac:structured-macro ac:macro-id="33c7bc80-5dd1-4da2-86a2-6a1dfe62d9bd" ac:name="card" ac:schema-version="1">
      <ac:parameter ac:name="label">Health Check Tools</ac:parameter>
      <ac:rich-text-body>
        <ac:structured-macro ac:macro-id="6f6d8ecb-8656-4227-a942-be01cbd482c5" ac:name="panel" ac:schema-version="1">
          <ac:parameter ac:name="borderColor">#36b37e</ac:parameter>
          <ac:parameter ac:name="bgColor">#fff</ac:parameter>
          <ac:parameter ac:name="titleBGColor">#e3fcef</ac:parameter>
          <ac:parameter ac:name="borderStyle">solid</ac:parameter>
          <ac:parameter ac:name="title">Available Health Checks</ac:parameter>
          <ac:rich-text-body>
            <ul>
              <li>
                <code>healthcheck</code>: Comprehensive JIRA configuration verification</li>
              <li>
                <code>bitbucket_healthcheck</code>: Bitbucket connectivity and auth verification</li>
              <li>
                <code>confluence_healthcheck</code>: Confluence connectivity and auth verification</li>
              <li>
                <code>test_connection</code>: JIRA authentication testing</li>
            </ul>
          </ac:rich-text-body>
        </ac:structured-macro>
      </ac:rich-text-body>
    </ac:structured-macro>
  </ac:rich-text-body>
</ac:structured-macro>
<hr/>
<h2>&#55357;&#56550; Dependencies</h2>
<ac:structured-macro ac:macro-id="5a279f22-9a7e-4aa1-a991-b8ec3dc3a743" ac:name="panel" ac:schema-version="1">
  <ac:parameter ac:name="borderColor">#0052cc</ac:parameter>
  <ac:parameter ac:name="bgColor">#f4f5f7</ac:parameter>
  <ac:parameter ac:name="titleBGColor">#deebff</ac:parameter>
  <ac:parameter ac:name="borderStyle">solid</ac:parameter>
  <ac:parameter ac:name="title">Required Dependencies</ac:parameter>
  <ac:rich-text-body>
    <ul>
      <li>
        <strong>fastmcp</strong> - Model Context Protocol framework</li>
      <li>
        <strong>requests</strong> - HTTP client for API interactions</li>
      <li>
        <strong>python-dotenv</strong> - Environment variable management</li>
      <li>
        <strong>langchain-community</strong> - Confluence content processing</li>
      <li>
        <strong>html2text</strong> - HTML to markdown conversion</li>
      <li>
        <strong>atlassian-python-api</strong> - Confluence API client</li>
      <li>
        <strong>pytest</strong> - Testing framework (development)</li>
      <li>
        <strong>black</strong> - Code formatting (development)</li>
      <li>
        <strong>flake8</strong> - Code linting (development)</li>
    </ul>
  </ac:rich-text-body>
</ac:structured-macro>
<hr/>
<h2>&#55357;&#56580; Platform Support</h2>
<table>
  <tbody>
    <tr>
      <th>
        <p>Platform</p>
      </th>
      <th>
        <p>Setup Script</p>
      </th>
      <th>
        <p>JIRA Support</p>
      </th>
      <th>
        <p>Bitbucket Support</p>
      </th>
      <th>
        <p>Confluence Support</p>
      </th>
    </tr>
    <tr>
      <td>
        <p>Windows</p>
      </td>
      <td>
        <p>
          <code>setup.ps1</code>
        </p>
      </td>
      <td>
        <p>
          <ac:emoticon ac:name="tick"/> Full</p>
      </td>
      <td>
        <p>
          <ac:emoticon ac:name="tick"/> Full</p>
      </td>
      <td>
        <p>
          <ac:emoticon ac:name="tick"/> Full</p>
      </td>
    </tr>
    <tr>
      <td>
        <p>Windows</p>
      </td>
      <td>
        <p>
          <code>setup.bat</code>
        </p>
      </td>
      <td>
        <p>
          <ac:emoticon ac:name="tick"/> Full</p>
      </td>
      <td>
        <p>
          <ac:emoticon ac:name="tick"/> Full</p>
      </td>
      <td>
        <p>
          <ac:emoticon ac:name="tick"/> Full</p>
      </td>
    </tr>
    <tr>
      <td>
        <p>macOS</p>
      </td>
      <td>
        <p>
          <code>setup.sh</code>
        </p>
      </td>
      <td>
        <p>
          <ac:emoticon ac:name="tick"/> Full</p>
      </td>
      <td>
        <p>
          <ac:emoticon ac:name="tick"/> Full</p>
      </td>
      <td>
        <p>
          <ac:emoticon ac:name="tick"/> Full</p>
      </td>
    </tr>
    <tr>
      <td>
        <p>Linux</p>
      </td>
      <td>
        <p>
          <code>setup.sh</code>
        </p>
      </td>
      <td>
        <p>
          <ac:emoticon ac:name="tick"/> Full</p>
      </td>
      <td>
        <p>
          <ac:emoticon ac:name="tick"/> Full</p>
      </td>
      <td>
        <p>
          <ac:emoticon ac:name="tick"/> Full</p>
      </td>
    </tr>
  </tbody>
</table>
<hr/>
<h2>&#55357;&#56960; Getting Started Checklist</h2>
<ac:structured-macro ac:macro-id="086717fd-b631-4a87-8d0c-b66fe9be3378" ac:name="deck" ac:schema-version="1">
  <ac:parameter ac:name="id">checklist-tabs</ac:parameter>
  <ac:rich-text-body>
    <ac:structured-macro ac:macro-id="547f5846-2f46-4cd8-894b-a74a9ba8b757" ac:name="card" ac:schema-version="1">
      <ac:parameter ac:name="label">Initial Setup</ac:parameter>
      <ac:rich-text-body>
        <ac:structured-macro ac:macro-id="2a310d5a-b689-4597-8bdb-c98f46370229" ac:name="panel" ac:schema-version="1">
          <ac:parameter ac:name="borderColor">#36b37e</ac:parameter>
          <ac:parameter ac:name="bgColor">#fff</ac:parameter>
          <ac:parameter ac:name="titleBGColor">#e3fcef</ac:parameter>
          <ac:parameter ac:name="borderStyle">solid</ac:parameter>
          <ac:parameter ac:name="title">Setup Checklist</ac:parameter>
          <ac:rich-text-body>
            <ul>
              <li>☐ Run platform-specific setup script</li>
              <li>☐ Generate JIRA API token</li>
              <li>☐ Generate Bitbucket authentication token</li>
              <li>☐ Generate Confluence API token</li>
              <li>☐ Update tokens in VSCode settings</li>
              <li>☐ Update usernames and URLs in settings</li>
              <li>☐ Restart IDE</li>
            </ul>
          </ac:rich-text-body>
        </ac:structured-macro>
      </ac:rich-text-body>
    </ac:structured-macro>
    <ac:structured-macro ac:macro-id="7ee01efa-5744-4d6d-ac9d-a601bc222fae" ac:name="card" ac:schema-version="1">
      <ac:parameter ac:name="label">Verification</ac:parameter>
      <ac:rich-text-body>
        <ac:structured-macro ac:macro-id="2b3e56ae-fd85-422b-a65e-79db69c86d38" ac:name="panel" ac:schema-version="1">
          <ac:parameter ac:name="borderColor">#0052cc</ac:parameter>
          <ac:parameter ac:name="bgColor">#fff</ac:parameter>
          <ac:parameter ac:name="titleBGColor">#deebff</ac:parameter>
          <ac:parameter ac:name="borderStyle">solid</ac:parameter>
          <ac:parameter ac:name="title">Verification Checklist</ac:parameter>
          <ac:rich-text-body>
            <ul>
              <li>☐ Run <code>healthcheck</code> tool (JIRA)</li>
              <li>☐ Run <code>test_connection</code> tool (JIRA)</li>
              <li>☐ Run <code>bitbucket_healthcheck</code> tool (Bitbucket)</li>
              <li>☐ Run <code>confluence_healthcheck</code> tool (Confluence)</li>
            </ul>
          </ac:rich-text-body>
        </ac:structured-macro>
      </ac:rich-text-body>
    </ac:structured-macro>
    <ac:structured-macro ac:macro-id="648cc783-e3dc-424c-bd03-df0ca95864e4" ac:name="card" ac:schema-version="1">
      <ac:parameter ac:name="label">First Usage</ac:parameter>
      <ac:rich-text-body>
        <ac:structured-macro ac:macro-id="cb24a6b8-3029-4b1e-9c05-f29099b3bf48" ac:name="panel" ac:schema-version="1">
          <ac:parameter ac:name="borderColor">#ff8b00</ac:parameter>
          <ac:parameter ac:name="bgColor">#fff</ac:parameter>
          <ac:parameter ac:name="titleBGColor">#fff4e6</ac:parameter>
          <ac:parameter ac:name="borderStyle">solid</ac:parameter>
          <ac:parameter ac:name="title">First Usage Checklist</ac:parameter>
          <ac:rich-text-body>
            <ul>
              <li>☐ Try <code>get_my_active_work</code> (JIRA)</li>
              <li>☐ Try <code>get_pr_details</code> with a sample PR URL (Bitbucket)</li>
              <li>☐ Try <code>search_confluence</code> with a sample query (Confluence)</li>
              <li>☐ Explore other tools based on your workflow needs</li>
            </ul>
          </ac:rich-text-body>
        </ac:structured-macro>
      </ac:rich-text-body>
    </ac:structured-macro>
  </ac:rich-text-body>
</ac:structured-macro>
<hr/>
<ac:structured-macro ac:macro-id="bc7c30ed-fa40-4992-80ad-af18813019bd" ac:name="panel" ac:schema-version="1">
  <ac:parameter ac:name="borderColor">#172b4d</ac:parameter>
  <ac:parameter ac:name="bgColor">#fff</ac:parameter>
  <ac:parameter ac:name="titleBGColor">#f4f5f7</ac:parameter>
  <ac:parameter ac:name="borderStyle">solid</ac:parameter>
  <ac:parameter ac:name="title">Environment Variables Summary</ac:parameter>
  <ac:rich-text-body>
    <p>The servers require these main environment variables:</p>
    <ul>
      <li>
        <strong>JIRA</strong>: <code>JIRA_AUTH_TOKEN</code>, <code>JIRA_BASE_URL</code>
      </li>
      <li>
        <strong>Bitbucket</strong>: <code>BITBUCKET_AUTH_TOKEN</code>, <code>BITBUCKET_BASE_URL</code>
      </li>
      <li>
        <strong>Confluence</strong>: <code>CONFLUENCE_USERNAME</code>, <code>CONFLUENCE_API_KEY</code>, <code>CONFLUENCE_BASE_URL</code>
      </li>
    </ul>
  </ac:rich-text-body>
</ac:structured-macro>
<ac:structured-macro ac:macro-id="4803597b-b1d1-45bf-a74d-5e716c2ec956" ac:name="info" ac:schema-version="1">
  <ac:parameter ac:name="title">Documentation Note</ac:parameter>
  <ac:rich-text-body>
    <p>
      <em>This documentation covers the complete JIRA, Bitbucket &amp; Confluence MCP Server functionality. For technical implementation details, refer to the source code in the respective service and tools modules.</em>
    </p>
  </ac:rich-text-body>
</ac:structured-macro>
<p>
  <br/>
</p>
