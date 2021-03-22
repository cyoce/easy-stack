stack = []
stack.instance_exec do
  def get
    out = pop
    return "(#{out})" if out.include?(' ')
    out
  end
  loop do
    begin
      input = gets&.chomp!
      exit! if !input
      input.each_char do |c|
        case c
        when 'F'
          push "F #{get} #{get}"


        when 'G'
          push "(G #{get} #{get})"


        when 'f'
          push "(f #{pop})"

        when 'g'
          push "(g #{pop})"

        when '~'
          self[-2..-1] = self[-2..-1].reverse

        when ':'
          push last


        when '!'
          pop

        when '@'
          self[0..-1] = []

        else
          push c
        end
      end
    rescue
      puts $!.full_message
    ensure
      puts "  [#{join(' ')}]"
    end
  end
end
