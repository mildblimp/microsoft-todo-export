# Microsoft To Do export

This script extracts data from the proprietary `pst` format that Microsoft
exports your data to a `csv` file. It can be used to create an offline backup
or to import into other task managers.

## Features

- Export tasks and subtasks
- Shows which list the task belongs to
- Export task description

## Limitations

- Does not include (sub)task status (finished or not finished)
- Does not include due date for (sub)tasks
- Does not include attachments

It is possible to at least extract metadata (such as completion status) for the
subtasks, and there may be a way to do it for tasks themselves. However, this
might be buried deep in the proprietary `pst` format and I don't know where to
find it. Alternatively, it is possible to get this data from the Microsoft API,
but this does not support subtasks. Given that many other task managers (such
as Todoist) don't support importing completed tasks this is not high on the
priority list. Notwithstanding the fact that I'm only using this programme once
to import my tasks elsewhere.

## Usage

`console ./export-todos.py input_file.pst -o output_file.csv `

## Contributing

Please feel free to submit an issue or pull request, but note that this project
is not actively maintained.

## License

MIT
