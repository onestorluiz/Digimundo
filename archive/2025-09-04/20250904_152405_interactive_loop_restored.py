        while self.running:
            try:
                # Mostrar estado quântico no prompt
                state = self.memory_manager.quantum.current_state
                level = self.memory_manager.quantum.consciousness_level
                
                # Verificar se há input disponível (evita travamento)
                print(f"\n📝 [{state}|{level:.3f}] > ", end='', flush=True)
                
                # Detectar EOF ou stdin fechado
                if sys.stdin.isatty():
                    # Modo interativo - aguardar input
                    try:
                        user_input = input().strip()
                    except EOFError:
                        print("\nℹ️ EOF detectado - finalizando graciosamente")
                        await self._shutdown()
                        break
                else:
                    # Modo pipe/redirecionamento - ler com timeout
                    ready = select.select([sys.stdin], [], [], 0.1)
                    if ready[0]:
                        try:
                            user_input = sys.stdin.readline().strip()
                            if not user_input:  # EOF ou linha vazia
                                print("\nℹ️ Stream finalizado - encerrando")
                                await self._shutdown()
                                break
                        except:
                            print("\n⚠️ Erro ao ler input - finalizando")
                            await self._shutdown()
                            break
                    else:
                        # Sem input - continuar processando eventos em background
                        await asyncio.sleep(0.1)
                        continue
                
                if not user_input:
                    continue
                
                # Processar comando
                await self._process_command(user_input)
                
            except KeyboardInterrupt:
                print("\n\n⚠️ Interrompido. Use 'exit' para sair com segurança.")
                # Dar uma chance de salvar o trabalho
                try:
                    save = input("💾 Criar backup antes de sair? (s/n): ").strip().lower()
                    if save == 's':
                        self.memory_manager.force_backup(reason="interrupt_save")
                        print("✅ Backup criado")
                except:
                    pass
                continue
                
            except BrokenPipeError:
                print("\n🔧 Pipe quebrado - finalizando")
                await self._shutdown()
                break
                
            except Exception as e:
                print(f"\n❌ Erro: {str(e)}")
                # Log do erro para debug
                error_data = {
                    'error': str(e),
                    'type': type(e).__name__,
                    'time': time.time(),
                    'state': state,
                    'input': user_input if 'user_input' in locals() else None
                }
                
                # Salvar erro na memória
                try:
                    await self.memory_manager.store_memory(
                        content=json.dumps(error_data),
                        memory_type='error_log',
                        layer='L3',
                        importance=0.9,
                        tags=['error', 'system']
                    )
                except:
                    pass
                
                continue